document.addEventListener('DOMContentLoaded', () => {
 // DOM Elements
 const configSection = document.getElementById('configSection');
 const trackedSection = document.getElementById('trackedSection');
 const crUrlSelect = document.getElementById('crUrlSelect');
 const customUrlInput = document.getElementById('customUrl');
 const saveConfigBtn = document.getElementById('saveConfigBtn');
 const emdrList = document.getElementById('emdrList');
 const clearListBtn = document.getElementById('clearListBtn');
 // Check if we have a configured URL
 chrome.storage.sync.get(['crUrl'], (config) => {
   if (!config.crUrl) {
     // Show config section prominently if no URL is set
     trackedSection.classList.add('hidden');
     configSection.classList.remove('hidden');
   } else {
     // Show both sections if URL is configured
     configSection.classList.remove('hidden');
     trackedSection.classList.remove('hidden');
     crUrlSelect.value = config.crUrl;
     loadTrackedEmdrs();
   }
 });
 // Save configuration
 saveConfigBtn.addEventListener('click', () => {
   const selectedUrl = crUrlSelect.value || customUrlInput.value.trim();
   if (!selectedUrl) {
     alert('Please select or enter a CR URL');
     return;
   }
   chrome.storage.sync.set({ crUrl: selectedUrl }, () => {
     alert(`CR URL saved: ${selectedUrl}`);
     configSection.classList.remove('hidden');
     trackedSection.classList.remove('hidden');
     loadTrackedEmdrs();
   });
 });
 // Load tracked EMDRs
 function loadTrackedEmdrs() {
   chrome.storage.local.get(['emdrIds'], (result) => {
     emdrList.innerHTML = '';
     const ids = result.emdrIds || [];
     if (ids.length === 0) {
       const li = document.createElement('li');
       li.textContent = 'No EMDRs being tracked';
       emdrList.appendChild(li);
     } else {
       ids.forEach(id => {
         const li = document.createElement('li');
         li.textContent = id;
         emdrList.appendChild(li);
       });
     }
   });
 }
 // Clear all tracked EMDRs
 clearListBtn.addEventListener('click', () => {
   if (confirm('Are you sure you want to clear all tracked EMDRs?')) {
     chrome.storage.local.set({ emdrIds: [] }, () => {
       loadTrackedEmdrs();
     });
   }
 });
});