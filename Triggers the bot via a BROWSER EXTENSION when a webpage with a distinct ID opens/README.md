# Triggers the bot via a BROWSER EXTENSION when a webpage with a distinct ID opens

This repository includes a browser extension that addresses the problem statement outlined below, along with a sample Node.js web server source code for testing the extension. The extension is compatible with both Chrome and Edge browsers. To use it, simply load it as an unpacked extension through the browser’s extension management page. 

**While this solution is specifically built for the sample site, the approach can be reused and adjusted according to your website’s structure and behavior.**

## 📌 Problem Statement
In many workflow-heavy web applications (e.g., service desks, CRMs, form-based portals), each page corresponds to a unique item identified by a label or field within the page, such as a Ticket ID, User ID, or Record Number.
We needed a solution that could intelligently trigger a bot based on this unique ID, with the following requirements:
   - 1️⃣ Trigger Only for New Unique IDs
      - Read the unique ID from a specific label or element in the webpage (e.g., #ticket-id).
      - If the ID has not been encountered before, trigger the bot.
      - If the ID was already processed and we're simply switching between pages (like viewing ID1, then ID2, then back to ID1), the bot should not retrigger unnecessarily.
   - 2️⃣ Retrigger on Content Edits
      - If the content related to a previously seen ID has been modified, and we open the page again, the bot must retrigger.
      - This ensures the bot always responds to meaningful changes, even for the same ID.


## 🧭 Typical Navigation Flow Example
Imagine navigating through these pages:
   - Open ID1 → Bot triggers ✅
   - Switch to ID2 → Bot triggers ✅
   - Back to ID1 → No trigger ❌ (already processed)
   - Edit ID1 → Open it again → Bot triggers ✅ (change detected)
   - Navigate around → Extension continues monitoring silently 👂

     
## ⚙️ How the Extension Works
   - 🔍 Step 1: Detect the Unique ID
   - The extension listens for DOM changes or page load events.
   - It extracts the unique ID from a known HTML element like:
      ```
      <label id="record-id">ID1</label>
      ```

## 📦 Step 2: Maintain a Local Cache
A cache is maintained using chrome.storage.local or in-memory storage.

Each ID is tracked along with a checksum or timestamp of the current state (to detect edits).

## 🤖 Step 3: Decide Whether to Trigger the Bot
```
If:

   The ID is new, or

   The page content has changed for an existing ID

Then:

   The bot is triggered via the bot deployment API call from the background script.

Else:

   No action is taken.
```
### Note
The Bot Deployment API requires authentication. The token will be retrieved from the logged session's local storage associated with the Control Room URL. If no active user session is found, the extension will automatically open a popup window prompting the user to log in to the Control Room.


## 🧠 Key Logic (Simplified Pseudocode)

   ```
   onPageLoad(() => {
     const id = document.querySelector("#record-id")?.textContent;
     const pageHash = computeContentHash();
   
     if (!id) return;
   
     const stored = getFromCache(id);
   
     if (!stored || stored.hash !== pageHash) {
       triggerBot(id);
       updateCache(id, pageHash);
     }
   });
   ```
## ✅ Benefits
   - 🚀 No duplicate triggers – Handles back-and-forth page navigation smartly.

   - 🛠️ Change-aware – Responds only when the ID content is updated.

   - 🔇 Silent Monitoring – Works seamlessly in the background without disrupting the user.

   - ⏱️ Efficient – Avoids redundant bot operations, saving system and network resources.



