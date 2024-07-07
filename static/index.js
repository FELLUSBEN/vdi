function startPc(PcId) {
  fetch("/start-pc", {
    method: "POST",
    body: JSON.stringify({ PcId: PcId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
function stopPc(PcId) {
  fetch("/stop-pc", {
    method: "POST",
    body: JSON.stringify({ PcId: PcId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}