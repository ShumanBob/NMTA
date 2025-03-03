// List to hold all available CS classes being read in from selected_classes.html
scheduledClasses = {};

// Add class to the schedule
function addClass(element) {
    className = element.getAttribute('data-class');
    days = element.getAttribute('data-days').split(',');
    time = element.getAttribute('data-time');
    semester = element.getAttribute('data-semester');
    if (semester == 'Spring') {
        element.classList.add('disabledSEM');
        return;
    }

    conflict = days.some(day => scheduledClasses[`${day}-${time}`]);

    // If there's a conflict, grey out the class and return
    if (conflict) {
        element.classList.add('disabled');
        return;
    }

    // Add class to the schedule
    days.forEach(day => {
        scheduleSlot = document.getElementById(`${day}-${time}`);
        if (scheduleSlot && scheduleSlot.textContent === "") {
            scheduleSlot.textContent = className;
            scheduleSlot.classList.add("scheduled-class");
            scheduleSlot.setAttribute("onclick", `removeClass('${className}', '${days.join(",")}', '${time}')`);
            scheduledClasses[`${day}-${time}`] = className;
        }
    });

    // Remove class from available list
    element.remove();
    updateAvailableClasses();
}

// Remove class from the schedule
function removeClass(className, days, time) {
    daysArray = days.split(',');

    // Remove class from all scheduled time slots
    daysArray.forEach(day => {
        scheduleSlot = document.getElementById(`${day}-${time}`);
        if (scheduleSlot && scheduleSlot.textContent === className) {
            scheduleSlot.textContent = "";
            scheduleSlot.classList.remove("scheduled-class");
            scheduleSlot.removeAttribute("onclick");
            delete scheduledClasses[`${day}-${time}`];
        }
    });

    // Add back the class to the available list only once
    availableList = document.getElementById("available-list");
    newItem = document.createElement("li");

    // Display the class name with its days and time
    newItem.textContent = `${className} (${days} at ${time})`;

    // Store the data attributes for re-selection
    newItem.setAttribute("data-class", className);
    newItem.setAttribute("data-days", days);
    newItem.setAttribute("data-time", time);
    newItem.setAttribute("onclick", "addClass(this)");

    // Append to the list
    availableList.appendChild(newItem);

    // Update available classes
    updateAvailableClasses();
}

// Update available classes
function updateAvailableClasses() {
    availableClasses = document.querySelectorAll('#available-list li');

    availableClasses.forEach((classItem) => {
        days = classItem.getAttribute('data-days').split(',');
        time = classItem.getAttribute('data-time');

        conflict = days.some(day => scheduledClasses[`${day}-${time}`]);

        if (conflict) {
            classItem.classList.add('disabled');
        } else {
            classItem.classList.remove('disabled');
        }
    });
}

// Initial call to update available classes status
updateAvailableClasses();
