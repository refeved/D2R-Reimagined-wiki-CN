/* 本地预览站的前端逻辑：全站搜索 + 语言记忆。无外部依赖。 */
(function () {
  "use strict";

  var root = document.documentElement.getAttribute("data-root") || ".";
  var lang = document.documentElement.getAttribute("lang") || "zh";
  try {
    localStorage.setItem("d2rr-lang", lang);
  } catch (e) {
    /* 隐私模式下忽略 */
  }

  var input = document.getElementById("q");
  var box = document.getElementById("results");
  if (!input || !box) return;

  var indexPromise = null;
  var items = [];
  var selected = -1;

  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch(root + "/assets/search.json")
        .then(function (r) {
          return r.json();
        })
        .catch(function () {
          return [];
        });
    }
    return indexPromise;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function urlFor(entry) {
    return root + "/" + entry.p + ".html";
  }

  function search(query) {
    var tokens = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (!tokens.length) return [];
    var hits = [];
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      var hay = (it.t + " " + it.x).toLowerCase();
      var ok = true;
      for (var j = 0; j < tokens.length; j++) {
        if (hay.indexOf(tokens[j]) === -1) {
          ok = false;
          break;
        }
      }
      if (!ok) continue;
      var inTitle = it.t.toLowerCase().indexOf(tokens[0]) !== -1;
      hits.push({ it: it, score: (inTitle ? 2 : 0) + (it.l === lang ? 1 : 0) });
    }
    hits.sort(function (a, b) {
      return b.score - a.score || a.it.t.length - b.it.t.length;
    });
    return hits.slice(0, 15).map(function (h) {
      return h.it;
    });
  }

  function render(list, query) {
    selected = -1;
    if (!list.length) {
      box.innerHTML = '<div class="r-empty">没有匹配 “' + escapeHtml(query) + '” 的页面</div>';
      box.hidden = false;
      return;
    }
    box.innerHTML = list
      .map(function (it) {
        var label = it.l === "zh" ? "中文" : "EN";
        return (
          '<a href="' + urlFor(it) + '">' +
          '<span class="r-title">' + escapeHtml(it.t) + "</span>" +
          '<span class="r-path">' + label + " · " + escapeHtml(it.p.split("/").slice(1).join("/")) + "</span>" +
          '<div class="r-snippet">' + escapeHtml(it.x.slice(0, 90)) + "</div>" +
          "</a>"
        );
      })
      .join("");
    box.hidden = false;
  }

  function move(delta) {
    var links = box.querySelectorAll("a");
    if (!links.length) return;
    if (selected >= 0) links[selected].classList.remove("sel");
    selected = (selected + delta + links.length) % links.length;
    links[selected].classList.add("sel");
    links[selected].scrollIntoView({ block: "nearest" });
  }

  input.addEventListener("input", function () {
    var query = input.value.trim();
    if (!query) {
      box.hidden = true;
      return;
    }
    loadIndex().then(function (data) {
      items = data;
      render(search(query), query);
    });
  });

  input.addEventListener("focus", function () {
    loadIndex();
  });

  input.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      move(1);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      move(-1);
    } else if (e.key === "Enter") {
      var links = box.querySelectorAll("a");
      if (selected >= 0 && links[selected]) {
        location.href = links[selected].href;
      } else if (links.length) {
        location.href = links[0].href;
      }
    } else if (e.key === "Escape") {
      box.hidden = true;
      input.blur();
    }
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest(".search")) box.hidden = true;
  });

  document.addEventListener("keydown", function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      input.focus();
      input.select();
    }
  });
})();
