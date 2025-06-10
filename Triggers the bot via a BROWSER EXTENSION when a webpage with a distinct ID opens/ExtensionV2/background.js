async function clearStoredCrUrl() {
  return new Promise((resolve) => {
    chrome.storage.sync.remove(['crUrl'], () => {
      if (chrome.runtime.lastError) {
        console.error('Error clearing CR URL:', chrome.runtime.lastError);
      } else {
        console.log('CR URL cleared from storage');
      }
      resolve();
    });
  });
}

async function getConfiguredCrUrl() {
  return new Promise((resolve) => {
    chrome.storage.sync.get(['crUrl'], (result) => {
      resolve(result.crUrl || null);
    });
  });
}

async function promptForCrUrl(reason = 'Configuration Required') {
  return new Promise((resolve) => {
    const popupUrl = chrome.runtime.getURL('popup.html');

    chrome.windows.create({
      url: popupUrl,
      type: 'popup',
      width: 400,
      height: 400,
      focused: true
    }, (window) => {
      if (chrome.runtime.lastError) {
        showNotification('Configuration Required', 'Please configure CR URL. Popup failed to open - check if popup.html exists.');
        resolve(null);
        return;
      }

      let isResolved = false;

      const listener = (changes, area) => {
        if (area === 'sync' && changes.crUrl && !isResolved) {
          isResolved = true;
          chrome.storage.onChanged.removeListener(listener);
          resolve(changes.crUrl.newValue);
        }
      };

      const windowRemovedListener = (windowId) => {
        if (windowId === window.id && !isResolved) {
          isResolved = true;
          chrome.storage.onChanged.removeListener(listener);
          chrome.windows.onRemoved.removeListener(windowRemovedListener);
          resolve(null);
        }
      };

      chrome.storage.onChanged.addListener(listener);
      chrome.windows.onRemoved.addListener(windowRemovedListener);

      // Timeout after 5 minutes
      setTimeout(() => {
        if (!isResolved) {
          isResolved = true;
          chrome.storage.onChanged.removeListener(listener);
          chrome.windows.onRemoved.removeListener(windowRemovedListener);

          // Check if window still exists before trying to close it
          chrome.windows.get(window.id, (windowInfo) => {
            if (!chrome.runtime.lastError && windowInfo) {
              chrome.windows.remove(window.id, () => {
                // Ignore any errors when closing
              });
            }
          });

          resolve(null);
        }
      }, 300000);
    });
  });
}

async function ensureCrUrlConfigured() {
  let crUrl = await getConfiguredCrUrl();

  if (crUrl) {
    try {
      new URL(crUrl);
      return crUrl;
    } catch (error) {
      crUrl = null;
    }
  }

  if (!crUrl) {
    crUrl = await promptForCrUrl('Configuration Required');
  }

  return crUrl;
}

function showNotification(title, message) {
  if (chrome.notifications?.create) {
    chrome.notifications.create({
      type: 'basic',
      iconUrl: chrome.runtime.getURL('icon.png'),
      title,
      message,
      priority: 2
    });
  }
}

chrome.tabs.onActivated.addListener(({ tabId }) => {
  chrome.tabs.get(tabId, (tab) => {
    if (chrome.runtime.lastError) return;
    if (tab && tab.url) {
      handleTabUrl(tab.url);
    }
  });
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url) {
    handleTabUrl(tab.url);
  }
});

function handleTabUrl(url) {
  const match = url.match(/\/apex\/EMDR\?id=(\d+)/);
  if (!match) return;
  const emdrId = match[1];
  const isEdit = url.includes("edit=true");
  if (isEdit) return;

  checkLoginAndProceed(emdrId).catch(error => {
    console.error("Error in EMDR processing chain:", error);
  });
}

async function checkLoginAndProceed(emdrId) {
  // First check if we have a configured CR URL
  const crUrl = await getConfiguredCrUrl();

  if (crUrl) {
    // We have a CR URL, so check for auth token
    const token = await checkCRAuthToken();
    if (token) {
      // Found token, proceed with processing
      await processEmdrId(emdrId, token);
      return;
    }
    // No token found - user is logged out, clear stored CR URL and show popup
    console.log("No auth token found, clearing stored CR URL and showing popup");
    await clearStoredCrUrl();
    await handleMissingToken(emdrId);
  } else {
    // No CR URL configured, show popup immediately
    await handleMissingToken(emdrId);
  }
}

async function checkCRAuthToken() {
  try {
    const crUrl = await getConfiguredCrUrl();
    if (!crUrl) {
      return null;
    }

    return new Promise((resolve) => {
      chrome.tabs.query({}, (allTabs) => {
        if (chrome.runtime.lastError) {
          resolve(null);
          return;
        }

        const cleanCrUrl = crUrl.replace(/\/+$/, '').toLowerCase();

        const matchingTabs = allTabs.filter(tab => {
          if (!tab.url) return false;

          try {
            const tabUrl = new URL(tab.url);
            const crUrlObj = new URL(cleanCrUrl);
            const hostMatch = tabUrl.hostname === crUrlObj.hostname;
            const protocolMatch = tabUrl.protocol === crUrlObj.protocol;
            const startsWithMatch = tab.url.toLowerCase().startsWith(cleanCrUrl);
            return (hostMatch && protocolMatch) || startsWithMatch;
          } catch (error) {
            return false;
          }
        });

        if (!matchingTabs.length) {
          resolve(null);
          return;
        }

        const targetTab = matchingTabs[0];

        chrome.scripting.executeScript({
          target: { tabId: targetTab.id },
          func: () => {
            let token = localStorage.getItem('authToken');

            if (token) {
              if (token.startsWith('"') && token.endsWith('"')) {
                token = token.slice(1, -1);
              }

              if (token.includes('\\"')) {
                token = token.replace(/\\"/g, '"');
              }

              if (token.startsWith('"') || token.startsWith('{')) {
                try {
                  const parsed = JSON.parse(token);
                  if (typeof parsed === 'string') {
                    token = parsed;
                  }
                } catch (e) {}
              }
            }

            return token;
          }
        }, (results) => {
          if (chrome.runtime.lastError) {
            resolve(null);
            return;
          }

          const token = results?.[0]?.result;

          if (token && token.length > 10) {
            resolve(token);
          } else {
            resolve(null);
          }
        });
      });
    });
  } catch (error) {
    return null;
  }
}

async function getApiUrl() {
  return new Promise((resolve) => {
    chrome.storage.sync.get(['crUrl'], function(result) {
      if (chrome.runtime.lastError) {
        resolve(null);
        return;
      }
      const crUrl = result.crUrl;
      if (!crUrl) {
        resolve(null);
        return;
      }

      const cleanUrl = crUrl.replace(/\/+$/, '');
      const apiUrl = `${cleanUrl}/v4/automations/deploy`;
      resolve(apiUrl);
    });
  });
}

async function handleMissingToken(emdrId) {

  showNotification('Configuration Required', 'Please configure your CR URL.');

  const crUrl = await promptForCrUrl('CR URL Configuration Required');
  if (!crUrl) {
    showNotification('Error', 'CR URL configuration cancelled');
    return;
  }


  const token = await checkCRAuthToken();
  if (token) {
    await processEmdrId(emdrId, token);
    return;
  }


  const existingCrTab = await findExistingCrTab(crUrl);
  let loginTab;

  if (existingCrTab) {
    loginTab = existingCrTab;
    await chrome.tabs.update(existingCrTab.id, { active: true });
  } else {
    try {
      loginTab = await new Promise((resolve, reject) => {
        chrome.tabs.create({ url: crUrl, active: false }, (tab) => {
          if (chrome.runtime.lastError) {
            reject(chrome.runtime.lastError);
          } else {
            resolve(tab);
          }
        });
      });

      setTimeout(() => {
        chrome.tabs.update(loginTab.id, { active: true });
      }, 1000);
    } catch (error) {
      showNotification('Invalid CR URL', 'Failed to open CR URL. Please try again.');
      return;
    }
  }

  showNotification('Login Required', 'Please login to CR in the opened tab');

  const newToken = await waitForTokenWithTimeout(300000);

  if (newToken) {
    await processEmdrId(emdrId, newToken);
  } else {
    showNotification('Login Timeout', 'Login did not complete in time. Please try again.');
   
    await clearStoredCrUrl();
  }
}

async function findExistingCrTab(crUrl) {
  return new Promise((resolve) => {
    chrome.tabs.query({}, (allTabs) => {
      if (chrome.runtime.lastError) {
        resolve(null);
        return;
      }

      const cleanCrUrl = crUrl.replace(/\/+$/, '').toLowerCase();

      const matchingTabs = allTabs.filter(tab => {
        if (!tab.url) return false;

        try {
          const tabUrl = new URL(tab.url);
          const crUrlObj = new URL(cleanCrUrl);
          const hostMatch = tabUrl.hostname === crUrlObj.hostname;
          const protocolMatch = tabUrl.protocol === crUrlObj.protocol;
          const startsWithMatch = tab.url.toLowerCase().startsWith(cleanCrUrl);
          return (hostMatch && protocolMatch) || startsWithMatch;
        } catch (error) {
          return false;
        }
      });

      if (matchingTabs.length > 0) {
        resolve(matchingTabs[0]);
      } else {
        resolve(null);
      }
    });
  });
}

async function waitForTokenWithTimeout(timeout) {
  return new Promise((resolve) => {
    const timer = setTimeout(() => {
      resolve(null);
    }, timeout);

    const checkInterval = setInterval(async () => {
      const token = await checkCRAuthToken();
      if (token) {
        clearTimeout(timer);
        clearInterval(checkInterval);
        resolve(token);
      }
    }, 2000);
  });
}

function processEmdrId(emdrId, token) {
  return new Promise((resolve, reject) => {
    chrome.storage.local.get(["emdrIds"], (result) => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
        return;
      }

      let emdrIds = result.emdrIds || [];

      if (!emdrIds.includes(emdrId)) {
        emdrIds.push(emdrId);
        chrome.storage.local.set({ emdrIds }, () => {
          if (chrome.runtime.lastError) {
            reject(chrome.runtime.lastError);
            return;
          }

          chrome.storage.local.get(["emdrIds"], (verifyResult) => {
            if (verifyResult.emdrIds && verifyResult.emdrIds.includes(emdrId)) {
              resolve(emdrId);
              callBotDeployAPI(emdrId, token);
            } else {
              reject(new Error("Failed to verify EMDR ID storage"));
            }
          });
        });
      } else {
        resolve(emdrId);
      }
    });
  });
}

async function callBotDeployAPI(emdrId, token) {
  const apiUrl = await getApiUrl();
  console.log(token);

  const payload = {
     "botId": 25251,
     "automationName": "SampleBot:" + emdrId,
     "description": "EMDR bot deployment via Chrome extension",
     "botLabel": "EMDR_Processing",
     "runElevated": true,
     "hideBotAgentUi": true,
     "callbackInfo": {
       "url": "https://callbackserver.com/storeBotExecutionStatus",
       "headers": {
         "X-Authorization": token
       }
     },
     "automationPriority": "PRIORITY_MEDIUM",
     "botInput": {
       "input": {
         "type": "STRING",
         "string": emdrId
       }
     },
     "unattendedRequest": {
       "runAsUserIds": ["237"],
       "poolIds": [],
       "numOfRunAsUsersToUse": "1",
       "deviceUsageType": "RUN_ONLY_ON_DEFAULT_DEVICE"
     }
   };

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Authorization': token
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    const data = await response.json();
    console.log("API Success:", data);
  } catch (error) {
    console.error("API Call Failed:", error);
  }
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  switch (request.action) {
    case 'getProcessedEmdrIds':
      chrome.storage.local.get(["emdrIds"], (result) => {
        sendResponse({ emdrIds: result.emdrIds || [] });
      });
      return true;

    case 'clearProcessedEmdrIds':
      chrome.storage.local.set({ emdrIds: [] }, () => {
        sendResponse({ success: true });
      });
      return true;

    case 'checkAuthToken':
      checkCRAuthToken().then((token) => {
        sendResponse({ token: token });
      }).catch((error) => {
        sendResponse({ error: error.message });
      });
      return true;

    case 'getCurrentCrUrl':
      getConfiguredCrUrl().then((crUrl) => {
        sendResponse({ crUrl: crUrl });
      }).catch((error) => {
        sendResponse({ error: error.message });
      });
      return true;

    case 'setCrUrl':
      if (request.crUrl) {
        chrome.storage.sync.set({ crUrl: request.crUrl }, () => {
          if (chrome.runtime.lastError) {
            sendResponse({ error: chrome.runtime.lastError.message });
          } else {
            sendResponse({ success: true });
          }
        });
      } else {
        sendResponse({ error: 'No CR URL provided' });
      }
      return true;

    case 'testCrUrl':
      if (request.crUrl) {
        try {
          new URL(request.crUrl);
          sendResponse({ valid: true });
        } catch (error) {
          sendResponse({ valid: false, error: 'Invalid URL format' });
        }
      } else {
        sendResponse({ valid: false, error: 'No URL provided' });
      }
      return true;

    case 'reconfigureCrUrl':
      promptForCrUrl('Manual Reconfiguration').then((newUrl) => {
        if (newUrl) {
          sendResponse({ success: true, newUrl: newUrl });
        } else {
          sendResponse({ success: false, error: 'Configuration cancelled' });
        }
      }).catch((error) => {
        sendResponse({ success: false, error: error.message });
      });
      return true;

    default:
      sendResponse({ error: 'Unknown action' });
  }
});

function debugStorage() {
  chrome.storage.local.get(null, (items) => {
    console.log("Current storage contents:", items);
  });
}