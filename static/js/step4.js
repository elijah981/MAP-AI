function updateSummaryLabel() {
  var user_id = getUserId();
  var summaryLabel = document.getElementById("summaryLabel");

  // Fetch the count of analyzed achievements from the step4 database
  fetch(`/step4/summary/count/${user_id}`)
    .then((response) => response.json())
    .then((data) => {
      var count = data.count;
      var summaryButton = document.getElementById("summaryButton");

      summaryLabel.innerHTML = `${count} of 8 achievements analyzed`;

      if (count < 8) {
        summaryButton.disabled = true;
      } else {
        summaryButton.disabled = false;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function goToSummary() {
  window.location.href = "/step4/summary";
}

function setReanalyzeValue() {
  document.getElementById("reanalyzeInput").value = "reanalyze";
}

function showAchievement() {
  var selectedAchievementId = document.getElementById(
    "selected_achievement"
  ).value;
  var selectedAchievementInput = document.getElementById(
    "selected_achievement_input"
  );
  selectedAchievementInput.value = selectedAchievementId;

  // Hide the Re-Analyze button
  var reanalyzeButton = document.getElementById("reanalyzeButton");
  reanalyzeButton.style.display = "none";

  fetch(`/step2/read/${selectedAchievementId}`)
    .then((response) => response.json())
    .then((data) => {
      var achievementDetailsText = document.getElementById(
        "achievementDetailsText"
      );
      if (data.length > 0) {
        achievementDetailsText.innerHTML = `
              <p>${data[6]}</p>
          `;
      } else {
        achievementDetailsText.innerHTML = `
              <p></p>
          `;
      }
      unpopulateTableEntries(); // Call the function to unpopulate the table entries
    });
}

function analyzeSelectedAchievement() {
  // Show the loading spinner
  var loadingSpinner = document.getElementById("loadingSpinner");
  loadingSpinner.style.display = "block";

  var selectedAchievementId = document.getElementById(
    "selected_achievement"
  ).value;
  var selectedAchievementDetails = document.getElementById(
    "achievementDetailsText"
  ).innerText;
  var reanalyze = ""; // Initialize the reanalyze parameter

  // Check if the reanalyze button is visible
  var reanalyzeButton = document.getElementById("reanalyzeButton");
  if (reanalyzeButton.style.display === "block") {
    reanalyze = "reanalyze"; // Set the reanalyze parameter to "reanalyze"
  }

  fetch(`/step4/analyze_selected_achievement`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      achievementId: selectedAchievementId,
      achievementDetails: selectedAchievementDetails,
      reanalyze: reanalyze,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      updateSelectedAchievementDetails(data["tagged_text"]);
      populateTableEntries(data["categories"]);

      // Show the Re-Analyze button
      var reanalyzeButton = document.getElementById("reanalyzeButton");
      reanalyzeButton.style.display = "block";

      // Hide the loading spinner
      loadingSpinner.style.display = "none";
    });
}

function updateSelectedAchievementDetails(data) {
  var achievementDetailsText = document.getElementById(
    "achievementDetailsText"
  );
  if (data.length > 0) {
    achievementDetailsText.innerHTML = `
              <p>${data}</p>
          `;
  } else {
    achievementDetailsText.innerHTML = "";
  }
}

function populateTableEntries(data) {
  // Iterate over the categories and subcategories in the response
  for (const category in data) {
    const subcategories = data[category];
    // Iterate over the subcategories
    for (const subcategory in subcategories) {
      var checkboxName = `category_${category
        .toLowerCase()
        .replace(/ /g, "")
        .replace(/,/g, "_")}_0_subcategory_${subcategory
        .toLowerCase()
        .replace(/ /g, "")
        .replace(/,/g, "_")}_checkbox`;
      checkboxName = checkboxName.replace(/&/g, "").replace(/\//g, "_");
      const checkbox = document.querySelector(`input[name="${checkboxName}"]`);
      // Check the checkbox if the subcategory is present in the response
      if (subcategories[subcategory].length > 0) {
        checkbox.checked = true;
      } else {
        checkbox.checked = false;
      }
    }
  }
}

function unpopulateTableEntries() {
  const checkboxes = document.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach((checkbox) => {
    checkbox.checked = false;
  });
}

$(document).ready(function () {
  // Call updateSummaryLabel() after the page loads
  updateSummaryLabel();

  // Prevent form submission when analyze button is clicked
  $("#analyzeButton").click(function (event) {
    event.preventDefault();
    analyzeSelectedAchievement();
  });

  $("#reanalyzeButton").click(function (event) {
    event.preventDefault();
    analyzeSelectedAchievement();
  });

  // Hide the Re-Analyze button initially
  var reanalyzeButton = document.getElementById("reanalyzeButton");
  reanalyzeButton.style.display = "none";

  // Show the Re-Analyze button when Initialize button is clicked again
  $("#analyzeButton").click(function () {
    reanalyzeButton.style.display = "block";
  });

  $("body").on("mouseenter", ".subject_matter", function () {
    $('[data-toggle="tooltip"]').tooltip();
  });
});
