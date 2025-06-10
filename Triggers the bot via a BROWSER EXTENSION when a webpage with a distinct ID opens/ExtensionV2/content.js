window.addEventListener("load", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const emdrId = urlParams.get("id");
  const isEdit = urlParams.get("edit");

  if (isEdit && emdrId) {
    const form = document.querySelector("form");
    if (form) {
      form.addEventListener("submit", () => {
        chrome.storage.local.get(["emdrIds"], (result) => {
          let emdrIds = result.emdrIds || [];
          const updated = emdrIds.filter(id => id !== emdrId);
          chrome.storage.local.set({ emdrIds: updated });
          console.log("Removed EMDR ID after save:", emdrId);
        });
      });
    }
  }
});
