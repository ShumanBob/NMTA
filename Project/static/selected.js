let scheduledClasses = {};

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
        scheduledClasses[day].push({
            name: className,
            startMin,
            endMin
        });

        const startHour = Math.floor(startMin / 60);
        const endHour = Math.floor(endMin / 60);

        for (let hour = startHour; hour <= endHour; hour++) {
            const slot = document.getElementById(`${day}-${hour}`);
            if (!slot) continue;

            const hourStart = hour * 60;
            const hourEnd = (hour + 1) * 60;

            if (timeRangesOverlap(startMin, endMin, hourStart, hourEnd)) {
                const block = document.createElement("div");
                block.className = "class-block";
                block.textContent = classDescription;

                const topPercent = Math.max(0, (Math.max(startMin, hourStart) - hourStart) / 60) * 100;
                const heightPercent = (Math.min(endMin, hourEnd) - Math.max(startMin, hourStart)) / 60 * 100;

                block.style.top = `${topPercent}%`;
                block.style.height = `${heightPercent}%`;

                block.addEventListener("click", () => removeClassFromSchedule(className));

                slot.appendChild(block);
            }
        }
    });

    // Update credit hours
    const creditValue = parseInt(element.getAttribute("data-credits"));
    const creditDisplay = document.getElementById("credit-hours");
    creditDisplay.textContent = parseInt(creditDisplay.textContent) + creditValue;
}

function removeClassFromSchedule(className) {
    Object.keys(scheduledClasses).forEach(day => {
        scheduledClasses[day] = scheduledClasses[day].filter(cls => cls.name !== className);
        for (let hour = 8; hour <= 20; hour++) {
            const slot = document.getElementById(`${day}-${hour}`);
            if (slot) {
                const blocksToRemove = Array.from(slot.getElementsByClassName("class-block"))
                    .filter(block => block.textContent === className || block.textContent.includes(className));
                blocksToRemove.forEach(block => slot.removeChild(block));
            }
        }
    });

    // Adjust credit hours
    const classElement = document.querySelector(`[data-class="${className}"]`);
    if (classElement) {
        const creditValue = parseInt(classElement.getAttribute("data-credits"));
        const creditDisplay = document.getElementById("credit-hours");
        creditDisplay.textContent = Math.max(0, parseInt(creditDisplay.textContent) - creditValue);
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

