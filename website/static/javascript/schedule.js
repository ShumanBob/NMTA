let scheduledClasses = {};
let totalCreditHours = 0; //initialize total credit hours to 0

function convertTimeToMinutes(timeString) {
    const [time, period] = timeString.trim().split(" ");
    let [hour, minute] = time.split(":").map(Number);
    if (period === "PM" && hour !== 12) hour += 12;
    if (period === "AM" && hour === 12) hour = 0;
    return hour * 60 + minute;
}

function parseDays(days) {
    const dayMap = {
        M: "monday",
        T: "tuesday",
        W: "wednesday",
        R: "thursday",
        F: "friday"
    };
    return Array.from(days).map(day => dayMap[day]);
}

function timeRangesOverlap(startA, endA, startB, endB) {
    return startA < endB && startB < endA;
}

function addClass(element) {
    const className = element.getAttribute('data-class');
    const days = element.getAttribute('data-days');
    const time = element.getAttribute('data-time');
    const classDescription = element.getAttribute('data-title');
    const creditValue = parseInt(element.getAttribute("data-credit_hours"));

    const parsedDays = parseDays(days);
    const [startStr, endStr] = time.split(' - ');
    const startMin = convertTimeToMinutes(startStr);
    const endMin = convertTimeToMinutes(endStr);

    const isScheduled = Object.values(scheduledClasses).some(dayArr =>
        dayArr.some(cls => cls.name === className)
    );
    if (isScheduled) {
        removeClassFromSchedule(className);
        return;
    }

    let conflict = false;
    parsedDays.forEach(day => {
        if (scheduledClasses[day]) {
            for (const scheduled of scheduledClasses[day]) {
                if (timeRangesOverlap(startMin, endMin, scheduled.startMin, scheduled.endMin)) {
                    conflict = true;
                    return;
                }
            }
        }
    });

    if (conflict) {
        showConflictModal();
        return;
    }

    // No conflict, schedule class
    parsedDays.forEach(day => {
        if (!scheduledClasses[day]) scheduledClasses[day] = [];
        scheduledClasses[day].push({ name: className, startMin, endMin });

        const column = document.getElementById(`${day}-column`);
        if (!column) return;

        const duration = endMin - startMin;
        const top = startMin - 480; // 8:00 AM is base (480 min)

        const block = document.createElement("div");
        block.className = "class-block";
        block.textContent = classDescription;
        block.style.top = `${top}px`;
        block.style.height = `${duration}px`;

        block.addEventListener("click", () => removeClassFromSchedule(className));
        column.appendChild(block);
    });

    // Update credit hours
    totalCreditHours += creditValue;
    updateCreditHoursDisplay();
}

function removeClassFromSchedule(className) {
    Object.keys(scheduledClasses).forEach(day => {
        scheduledClasses[day] = scheduledClasses[day].filter(cls => cls.name !== className);
        const column = document.getElementById(`${day}-column`);
        if (column) {
            const blocksToRemove = Array.from(column.getElementsByClassName("class-block"))
                .filter(block => block.textContent === className || block.textContent.includes(className));
            blocksToRemove.forEach(block => column.removeChild(block));
        }
    });

    const classElement = document.querySelector(`[data-class="${className}"]`);
    if (classElement) {
        const creditValue = parseInt(classElement.getAttribute("data-credit_hours"));
        totalCreditHours = Math.max(0, totalCreditHours - creditValue);
        updateCreditHoursDisplay();
    }
}

function showConflictModal() {
    const modal = document.createElement("div");
    modal.style.position = "fixed";
    modal.style.top = "50%";
    modal.style.left = "50%";
    modal.style.transform = "translate(-50%, -50%)";
    modal.style.padding = "20px";
    modal.style.backgroundColor = "#fff";
    modal.style.border = "2px solid #333";
    modal.style.borderRadius = "10px";
    modal.style.zIndex = "1000";
    modal.style.boxShadow = "0px 4px 10px rgba(0, 0, 0, 0.2)";

    const closeButton = document.createElement("button");
    closeButton.textContent = "X";
    closeButton.style.position = "absolute";
    closeButton.style.top = "5px";
    closeButton.style.right = "10px";
    closeButton.style.fontSize = "18px";
    closeButton.style.cursor = "pointer";
    closeButton.style.backgroundColor = "#ff4c4c";
    closeButton.style.border = "none";
    closeButton.style.color = "white";
    closeButton.style.borderRadius = "50%";
    closeButton.onclick = () => document.body.removeChild(modal);

    const message = document.createElement("p");
    message.textContent = "You already have a class scheduled at that time!";
    message.style.fontSize = "16px";
    message.style.color = "#333";
    message.style.textAlign = "center";

    modal.appendChild(closeButton);
    modal.appendChild(message);
    document.body.appendChild(modal);
}

function updateCreditHoursDisplay() {
    document.getElementById("credit-hours").textContent = totalCreditHours;
}

document.getElementById("copy-crns-btn").addEventListener("click", () => {
    const crns = new Set();

    Object.keys(scheduledClasses).forEach(day => {
        scheduledClasses[day].forEach(cls => {
            const classElement = document.querySelector(`[data-class="${cls.name}"]`);
            if (classElement) {
                const crn = classElement.getAttribute("data-crn");
                if (crn) crns.add(crn);
            }
        });
    });

    const crnList = Array.from(crns).join(" ");
    if (crnList.length === 0) {
        alert("Add a class first.");
        return;
    }

    navigator.clipboard.writeText(crnList).then(() => {
        alert("Copied:\n" + crnList);
    }).catch(err => {
        console.error("Copy failed: ", err);
        alert("Failed to copy CRNs.");
    });
});
