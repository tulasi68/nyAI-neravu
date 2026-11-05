(function () {
  var total = 9;
  var current = 0;
  var visited = {};
  visited[0] = true;
  var events = [{ time: "Session start", text: "Opened the Nyai-Neravu workflow mock-up; all data is fictional." }];

  function $(id) { return document.getElementById(id); }

  function safe(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      var map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
      return map[c] || c;
    });
  }

  function toast(msg) {
    var el = $("toast");
    if (!el) return;
    el.textContent = msg;
    el.classList.remove("hidden");
    clearTimeout(window.__toastTimer);
    window.__toastTimer = setTimeout(function () {
      el.classList.add("hidden");
    }, 2600);
  }

  function log(text) {
    events.unshift({
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      text: text
    });
    renderLog();
  }

  function renderLog() {
    var el = $("auditLog");
    if (!el) return;
    el.innerHTML = events.map(function (e) {
      return '<div class="auditrow"><time>' + safe(e.time) + '</time><div>' + safe(e.text) + '</div></div>';
    }).join("");
  }

  function navigate(n) {
    current = Math.max(0, Math.min(total - 1, n));
    var steps = document.querySelectorAll(".step");
    for (var i = 0; i < steps.length; i++) {
      if (i === current) steps[i].classList.remove("hidden");
      else steps[i].classList.add("hidden");
    }
    var buttons = document.querySelectorAll(".stepnav button");
    for (var j = 0; j < buttons.length; j++) {
      if (j === current) buttons[j].classList.add("active");
      else buttons[j].classList.remove("active");
    }
    visited[current] = true;
    var visitedCount = 0;
    for (var k in visited) {
      if (Object.prototype.hasOwnProperty.call(visited, k)) visitedCount++;
    }
    var bar = $("progressbar");
    if (bar) bar.style.width = (visitedCount / total * 100) + "%";
    var metric = $("metricStage");
    if (metric) metric.textContent = (visitedCount - 1) + " / 8";
    var prevBtn = $("prevBtn");
    var nextBtn = $("nextBtn");
    if (prevBtn) prevBtn.disabled = current === 0;
    if (nextBtn) nextBtn.disabled = current === total - 1;
    var stepActions = document.querySelector(".stepactions");
    if (stepActions) {
      if (current === 0) stepActions.classList.add("hidden");
      else stepActions.classList.remove("hidden");
    }
    if (current === 8) renderLog();
    window.scrollTo(0, 0);
  }

  document.querySelectorAll("[data-step]").forEach(function (b) {
    b.addEventListener("click", function () {
      navigate(Number(b.getAttribute("data-step")));
    });
  });
  document.querySelectorAll("[data-go]").forEach(function (b) {
    b.addEventListener("click", function () {
      navigate(Number(b.getAttribute("data-go")));
    });
  });
  document.querySelectorAll("[data-back]").forEach(function (b) {
    b.addEventListener("click", function () {
      navigate(current - 1);
    });
  });
  var prevBtn = $("prevBtn");
  var nextBtn = $("nextBtn");
  if (prevBtn) prevBtn.addEventListener("click", function () { navigate(current - 1); });
  if (nextBtn) nextBtn.addEventListener("click", function () { navigate(current + 1); });

  function save(label) {
    log(label);
    toast(label + " (browser session only)");
  }

  function bindSave(id, label) {
    var el = $(id);
    if (el) el.addEventListener("click", function () { save(label); });
  }
  bindSave("saveIntake", "Demo intake saved");
  bindSave("saveEvidence", "Demo evidence and chronology saved");
  bindSave("saveLaw", "Legal research placeholder saved");
  bindSave("saveA", "Party A submission recorded");
  bindSave("saveB", "Party B response recorded");
  bindSave("saveHearing", "Hearing record saved");
  bindSave("savePanel", "Simulated AI panel statuses saved");
  bindSave("saveDraft", "Draft package saved");
  bindSave("recordHumanReview", "Human review action recorded (no legal effect)");

  function reset() {
    visited = {};
    visited[0] = true;
    events = [{ time: "Session start", text: "Demo reset; all data remains fictional." }];
    navigate(0);
    toast("Demo reset");
  }
  var r1 = $("resetDemo");
  if (r1) r1.addEventListener("click", reset);
  var r2 = $("resetDemo2");
  if (r2) r2.addEventListener("click", reset);

  navigate(0);
})();
