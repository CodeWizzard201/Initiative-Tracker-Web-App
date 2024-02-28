const editButtons = document.querySelectorAll(".edit-button");
const deleteButtons = document.querySelectorAll(".delete-button");
const createCombatantForm = document.getElementById("create-combatant-form");

createCombatantForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const formData = new FormData(createCombatantForm);
    console.log(formData);
    fetch("/create_combatant", {
        method:"POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){
            window.location.href = "http://redwizard.pythonanywhere.com/";
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error("Error creating combatant:", error);
        alert("An error occured while creating a combatant. Please try again.");
    });
});

editButtons.forEach(button => {
    button.addEventListener("click", async (event) => {
        const combatantID = button.dataset.combatantId;
        const response = await fetch(`/get_combatant/${ combatantID }`, {
            method: "GET",
            headers: { "Content-Type": 'application/json'}
        }); // Fetch combatant details
        const combatant = await response.json();

        // Set modal input values
        document.getElementById("edit-combatant-form").dataset.combatantId = combatantID;
        document.getElementById("edit-name").value = combatant.name;
        document.getElementById("edit-modifier").value = combatant.mod;
        document.getElementById("edit-roll").value = combatant.roll;
    });
});

const editForm = document.getElementById("edit-combatant-form");

editForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent default form submission

    // Extract updated combatant data
    const editedCombatant = {
        id: editForm.dataset.combatantId,
        name: document.getElementById("edit-name").value,
        mod: document.getElementById("edit-modifier").value,
        roll: document.getElementById("edit-roll").value
    };

    // Send update request to Flask backend
    const response = await fetch("/update_combatant", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(editedCombatant)
    });

    if (response.ok) {
        // Refresh page on successful response
        $("#edit-modal").modal("hide"); // Close the modal
        window.location.href = "http://redwizard.pythonanywhere.com/";

    } else {
        console.error("Error updating combatant:", response.statusText);
    }
});

deleteButtons.forEach(button => {
    button.addEventListener("click", () => {
        const combatantID = button.dataset.combatantId;
        fetch("/delete_combatant", {
            method: "POST",
            headers: { "Content-Type": 'application/json'},
            body: JSON.stringify({"combatantID": combatantID})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}`);  // Throw error for non-200 status
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                button.closest(".combatant-entry").remove();  // Remove from DOM
            } else {
                // Handle specific error message from server
                alert(data.error);
            }
        })
        .catch(error => {
            console.error("Error deleting combatant:", error);
            alert("An error occurred while deleting the combatant. Please try again.");
        });
    });
});