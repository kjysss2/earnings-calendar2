(async function () {
  const calendar = document.getElementById("calendar");
  const title = document.getElementById("calendarTitle");
  const dateRow = document.getElementById("dateRow");
  const companyRow = document.getElementById("companyRow");
  const loadError = document.getElementById("loadError");

  try {
    const response = await fetch("data/calendar.json", { cache: "no-store" });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    render(data);
  } catch (error) {
    calendar.classList.add("is-error");
    loadError.hidden = false;
  }

  function render(data) {
    const columns = Array.isArray(data.columns) ? data.columns : [];

    title.textContent = data.title || "한국 잠정실적발표 일정(변동 가능)";
    dateRow.innerHTML = "";
    companyRow.innerHTML = "";

    const month = document.createElement("div");
    month.className = "month-label";
    month.textContent = data.monthLabel || "7월";
    dateRow.append(month);

    for (const column of columns) {
      const cell = document.createElement("div");
      cell.className = "date-cell";
      cell.textContent = column.label || "";
      dateRow.append(cell);
    }

    const spacer = document.createElement("div");
    spacer.className = "company-spacer";
    companyRow.append(spacer);

    for (const column of columns) {
      const list = document.createElement("div");
      list.className = "company-list";

      const ul = document.createElement("ul");
      const companies = Array.isArray(column.companies) ? column.companies : [];

      for (const company of companies) {
        const li = document.createElement("li");

        if (company.highlight) {
          li.className = "highlight";
        }

        li.textContent = company.name || "";
        ul.append(li);
      }

      list.append(ul);
      companyRow.append(list);
    }
  }
}());
