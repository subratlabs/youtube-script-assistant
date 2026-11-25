const videoForm = document.getElementById("video-form");

videoForm.addEventListener("submit", async function (event) {
event.preventDefault();

const createPlanBtn = document.getElementById("create-video-plan-btn");
const originalButtonText = createPlanBtn.textContent;

createPlanBtn.disabled = true;
createPlanBtn.textContent = "Generating Video Plan...";

const formData = {
    topic: document.getElementById("topic").value,
    target_audience: document.getElementById("target-audience").value,
    language: document.getElementById("language").value,
    duration: Number(document.getElementById("duration").value),
    content_type: document.getElementById("content-type").value,
    tone: document.getElementById("tone").value,
    instructions: document.getElementById("instructions").value || null
};

try {
    const response = await fetch(
        "http://127.0.0.1:8000/api/generate-titles",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        }
    );

    const result = await response.json();

    if (!response.ok) {
        throw new Error(JSON.stringify(result.detail || result));
    }

    console.log("Generated titles:", result);

    const titlesList = document.getElementById("titles-list");
    titlesList.replaceChildren();

    const titles = Array.isArray(result)
        ? result
        : result.titles;

    if (!Array.isArray(titles)) {
        throw new Error("Unexpected response format. Check the API response.");
    }

    titles.forEach(function (title) {
        const titleElement = document.createElement("p");
       const titleText =
    typeof title === "string" ? title : title.title;

titleElement.textContent = titleText;
titleElement.style.cursor = "pointer";

titleElement.addEventListener("click", function () {
    document.querySelectorAll("#titles-list p").forEach(function (item) {
        item.style.backgroundColor = "";
    });

    titleElement.style.backgroundColor = "#ddd6fe";
    window.selectedTitle = titleText;
});

        titlesList.appendChild(titleElement);
    });

    // Generate opening hooks
    const hooksResponse = await fetch(
        "http://127.0.0.1:8000/api/generate-hooks",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        }
    );

    const hooksResult = await hooksResponse.json();

    if (!hooksResponse.ok) {
        throw new Error(JSON.stringify(hooksResult.detail || hooksResult));
    }

    console.log("Generated hooks:", hooksResult);

    const hooksList = document.getElementById("hooks-list");
    hooksList.replaceChildren();

    const hooks = Array.isArray(hooksResult)
        ? hooksResult
        : hooksResult.hooks || hooksResult.opening_hooks;

    if (!Array.isArray(hooks)) {
        throw new Error("Unexpected hooks response format. Check the API response.");
    }

    hooks.forEach(function (hook) {
        const hookElement = document.createElement("p");

        const hookText =
    typeof hook === "string"
        ? hook
        : hook.hook || hook.text || hook.title;

hookElement.textContent = hookText;
hookElement.style.cursor = "pointer";

hookElement.addEventListener("click", function () {
    document.querySelectorAll("#hooks-list p").forEach(function (item) {
        item.style.backgroundColor = "";
    });

    hookElement.style.backgroundColor = "#ddd6fe";
    window.selectedHook = hookText;
});

        hooksList.appendChild(hookElement);
    });


    // Generate video outline
    const outlineResponse = await fetch(
        "http://127.0.0.1:8000/api/generate-outline",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        }
    );

    const outlineResult = await outlineResponse.json();

    if (!outlineResponse.ok) {
        throw new Error(
            JSON.stringify(outlineResult.detail || outlineResult)
        );
    }

    console.log("Generated outline:", outlineResult);

    const outlineList = document.getElementById("outline-list");
    outlineList.replaceChildren();

    const outline = outlineResult.outline;

    if (!Array.isArray(outline)) {
        throw new Error("Unexpected outline response format.");
    }

    outline.forEach(function (item) {
        const outlineElement = document.createElement("p");
        outlineElement.textContent = item;
        outlineList.appendChild(outlineElement);
    });

} catch (error) {
    console.error("Video plan generation failed:", error);

    if (error instanceof TypeError && error.message === "Failed to fetch") {
        alert(
            "Unable to connect to the server. Please ensure the backend is running and try again."
        );
    } else {
        const message = error.message || "";

        if (message.includes("503")) {
            alert(
                "The AI service is temporarily unavailable. Please try again later."
            );
        } else if (message.includes("502")) {
            alert(
                "The AI service returned an invalid response. Please try again."
            );
        } else {
            alert("Could not generate the video plan. Please try again.");
        }
    }
} finally {
    createPlanBtn.disabled = false;
    createPlanBtn.textContent = originalButtonText;
}
});

const generateScriptButton = document.getElementById("generate-script-btn");

generateScriptButton.addEventListener("click", async function () {
    if (!window.selectedTitle) {
        alert("Please select a video title first.");
        return;
    }

    if (!window.selectedHook) {
        alert("Please select an opening hook first.");
        return;
    }

    const outlineElements = document.querySelectorAll("#outline-list p");
    const outline = Array.from(outlineElements).map(function (item) {
        return item.textContent;
    });

    if (outline.length === 0) {
        alert("Please generate the video outline first.");
        return;
    }

    const formData = {
        topic: document.getElementById("topic").value,
        target_audience: document.getElementById("target-audience").value,
        language: document.getElementById("language").value,
        duration: Number(document.getElementById("duration").value),
        content_type: document.getElementById("content-type").value,
        tone: document.getElementById("tone").value,
        instructions: document.getElementById("instructions").value || null,
        selected_title: window.selectedTitle,
        selected_hook: window.selectedHook,
        outline: outline
    };

    try {
        generateScriptButton.disabled = true;
        generateScriptButton.textContent = "Generating Script...";

        const response = await fetch(
            "http://127.0.0.1:8000/api/generate-script",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(JSON.stringify(result.detail || result));
        }

        document.getElementById("script-editor").value = result.script;

        const scriptContainer = document.getElementById("script-content");
scriptContainer.replaceChildren();

const sections = result.script
    .replace(/\r\n/g, "\n")
    .split(/(?=\[(?:INTRODUCTION|MAIN CONTENT:|CONCLUSION AND CTA)\])/i)
    .map(section => section.trim())
    .filter(Boolean);

sections.forEach(function (sectionText) {
    const match = sectionText.match(
        /^\[(INTRODUCTION|MAIN CONTENT:\s*[^\]]+|CONCLUSION AND CTA)\]\s*/i
    );

    const card = document.createElement("div");
    card.className = "script-section-card";

    let bodyText = sectionText;

    if (match) {
        const heading = document.createElement("h3");
        heading.textContent = match[1]
            .replace(/^MAIN CONTENT:\s*/i, "")
            .replace(/\b\w/g, char => char.toUpperCase());

        card.appendChild(heading);
        bodyText = sectionText.slice(match[0].length).trim();
    }

    if (bodyText) {
        const body = document.createElement("p");
        body.textContent = bodyText;
        card.appendChild(body);
    }

    if (card.children.length > 0) {
        scriptContainer.appendChild(card);
    }
});

        const scriptStats = document.createElement("p");
        scriptStats.textContent =
            "Word count: " + result.word_count +
            " | Estimated duration: " + result.estimated_duration + " minutes";

        document.getElementById("script-content").appendChild(scriptStats);

        console.log("Generated script:", result);

    } catch (error) {
        console.error("Script generation failed:", error);
        alert("Could not generate the full script. Check the browser console.");
    } finally {
        generateScriptButton.disabled = false;
        generateScriptButton.textContent = "Generate Full Script";
    }
});



const generateVisualsButton = document.getElementById("generate-visuals-btn");

generateVisualsButton.addEventListener("click", async function () {
    if (!window.selectedTitle) {
        alert("Please select a video title first.");
        return;
    }

    const scriptContent = document.getElementById("script-content");
    const scriptText = scriptContent.querySelectorAll(
    ".script-section-card p"
);

const fullScript = Array.from(scriptText)
    .map(paragraph => paragraph.textContent.trim())
    .filter(Boolean)
    .join("\n\n");

   if (!fullScript) {
    alert("Please generate the full script first.");
    return;
}
    

    const formData = {
        topic: document.getElementById("topic").value,
        target_audience: document.getElementById("target-audience").value,
        language: document.getElementById("language").value,
        duration: Number(document.getElementById("duration").value),
        content_type: document.getElementById("content-type").value,
        tone: document.getElementById("tone").value,
        instructions: document.getElementById("instructions").value || null,
        selected_title: window.selectedTitle,
        script: fullScript
    };

    try {
        generateVisualsButton.disabled = true;
        generateVisualsButton.textContent = "Generating Visuals...";

        const response = await fetch(
            "http://127.0.0.1:8000/api/generate-visuals",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(JSON.stringify(result.detail || result));
        }

        const visualsList = document.getElementById("visuals-list");
        visualsList.replaceChildren();

        result.visuals.forEach(function (item) {
            const card = document.createElement("div");
            card.className = "visual-card";

            const section = document.createElement("h4");
            section.textContent = item.section;

            const visual = document.createElement("p");
            visual.textContent = "Visual: " + item.visual;

            const bRoll = document.createElement("p");
            bRoll.textContent = "B-roll: " + item.b_roll;

            const onScreenText = document.createElement("p");
            onScreenText.textContent =
                "On-screen text: " + item.on_screen_text;

            card.append(section, visual, bRoll, onScreenText);
            visualsList.appendChild(card);
        });

        console.log("Generated visuals:", result);

    } catch (error) {
        console.error("Visual generation failed:", error);
        alert("Could not generate visual suggestions. Check the browser console.");
    } finally {
        generateVisualsButton.disabled = false;
        generateVisualsButton.textContent = "Generate Visual Suggestions";
    }
});



const generateDescriptionButton = document.getElementById("generate-description-btn");

generateDescriptionButton.addEventListener("click", async function () {
    if (!window.selectedTitle) {
        alert("Please select a video title first.");
        return;
    }

    const scriptContent = document.getElementById("script-content");

const scriptParagraphs = scriptContent.querySelectorAll(
    ".script-section-card p"
);

const fullScript = Array.from(scriptParagraphs)
    .map(paragraph => paragraph.textContent.trim())
    .filter(Boolean)
    .join("\n\n");

   if (!fullScript) {
    alert("Please generate the full script first.");
    return;
}

    const formData = {
        topic: document.getElementById("topic").value,
        target_audience: document.getElementById("target-audience").value,
        language: document.getElementById("language").value,
        duration: Number(document.getElementById("duration").value),
        content_type: document.getElementById("content-type").value,
        tone: document.getElementById("tone").value,
        instructions: document.getElementById("instructions").value || null,
        selected_title: window.selectedTitle,
        script: fullScript
    };

    try {
        generateDescriptionButton.disabled = true;
        generateDescriptionButton.textContent = "Generating Description...";

        const response = await fetch(
            "http://127.0.0.1:8000/api/generate-description",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(JSON.stringify(result.detail || result));
        }

        const descriptionContent = document.getElementById("description-content");
        descriptionContent.replaceChildren();

        function addDescriptionField(label, value) {
            const heading = document.createElement("h4");
            heading.textContent = label;

            const paragraph = document.createElement("p");
            paragraph.textContent = Array.isArray(value)
                ? value.join(", ")
                : value;

            descriptionContent.append(heading, paragraph);
        }

        addDescriptionField("Introduction", result.intro);
        addDescriptionField("Summary", result.summary);
        addDescriptionField("Topics", result.topics);
        addDescriptionField("Keywords", result.keywords);
        addDescriptionField("Hashtags", result.hashtags);
        addDescriptionField("Call to Action", result.cta);

        console.log("Generated description:", result);

    } catch (error) {
        console.error("Description generation failed:", error);
        alert("Could not generate the YouTube description. Check the browser console.");
    } finally {
        generateDescriptionButton.disabled = false;
        generateDescriptionButton.textContent = "Generate YouTube Description";
    }
});


const regenerateSectionButton = document.getElementById("regenerate-section-btn");

regenerateSectionButton.addEventListener("click", async function () {
    if (!window.selectedTitle) {
        alert("Please select a video title first.");
        return;
    }

    const sectionName = document.getElementById("section-name").value.trim();
    const currentSection = document.getElementById("current-section").value.trim();

    const scriptContent = document.getElementById("script-content");

const scriptParagraphs = scriptContent.querySelectorAll(
    ".script-section-card p"
);

const fullScript = Array.from(scriptParagraphs)
    .map(paragraph => paragraph.textContent.trim())
    .filter(Boolean)
    .join("\n\n");

    if (!sectionName || sectionName.length < 2) {
        alert("Please enter a valid section name.");
        return;
    }

    if (!currentSection || currentSection.length < 10) {
        alert("Please enter at least 10 characters of section text.");
        return;
    }
if (fullScript.length < 50) {
    alert("Please generate the full script first.");
    return;
}

    const formData = {
        topic: document.getElementById("topic").value,
        target_audience: document.getElementById("target-audience").value,
        language: document.getElementById("language").value,
        duration: Number(document.getElementById("duration").value),
        content_type: document.getElementById("content-type").value,
        tone: document.getElementById("tone").value,
        instructions: document.getElementById("instructions").value || null,
        selected_title: window.selectedTitle,
        section_name: sectionName,
        current_section: currentSection,
        full_script: fullScript
    };

    try {
        regenerateSectionButton.disabled = true;
        regenerateSectionButton.textContent = "Regenerating...";

        const response = await fetch(
            "http://127.0.0.1:8000/api/regenerate-section",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(JSON.stringify(result.detail || result));
        }

        const resultContainer = document.getElementById("regenerated-section-result");
        resultContainer.replaceChildren();

        const heading = document.createElement("h4");
        heading.textContent = result.section_name;

        const paragraph = document.createElement("p");
        paragraph.textContent = result.regenerated_section;

        resultContainer.append(heading, paragraph);

        console.log("Regenerated section:", result);

    } catch (error) {
        console.error("Section regeneration failed:", error);
        alert("Could not regenerate the section. Check the browser console.");
    } finally {
        regenerateSectionButton.disabled = false;
        regenerateSectionButton.textContent = "Regenerate Section";
    }
});



const copyScriptBtn = document.getElementById("copy-script-btn");

copyScriptBtn.addEventListener("click", async function () {
    const scriptContent = document.getElementById("script-content");

    const editor = document.getElementById("script-editor");

    const fullScript = editor.value.trim();

    if (!fullScript) {
        alert("Please generate a script first.");
        return;
    }

    try {
        await navigator.clipboard.writeText(fullScript);
        alert("Full script copied successfully!");
    } catch (error) {
        alert("Unable to copy the script. Please try again.");
        console.error("Copy error:", error);
    }
});

const downloadScriptBtn = document.getElementById("download-script-btn");

downloadScriptBtn.addEventListener("click", function () {
    console.log("Download button clicked");

    const editor = document.getElementById("script-editor");
    const topicInput = document.getElementById("topic");

    const fullScript = editor.value.trim();
    const topic = topicInput?.value.trim() || "YouTube Script";

    if (!fullScript) {
        alert("Please generate or enter a script first.");
        return;
    }

    // Create a clean filename from the video topic
    const safeFilename = topic
        .replace(/[<>:"/\\|?*\x00-\x1F]/g, "")
        .trim()
        .replace(/\s+/g, "_")
        .slice(0, 100) || "YouTube_Script";

    // Format the exported script
    const formattedScript = [
        "=".repeat(50),
        topic.toUpperCase(),
        "=".repeat(50),
        "",
        "Generated with: YouTube Script Assistant",
        "",
        "-".repeat(50),
        "",
        fullScript,
        "",
        "=".repeat(50),
        "End of Script",
        "=".repeat(50)
    ].join("\n");

    const blob = new Blob([formattedScript], {
        type: "text/plain;charset=utf-8"
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = `${safeFilename}_Script.txt`;

    document.body.appendChild(link);
    link.click();
    link.remove();

    setTimeout(function () {
        URL.revokeObjectURL(url);
    }, 1000);
});


const saveScriptButton = document.getElementById("save-script-btn");

saveScriptButton.addEventListener("click", function () {
    const editedScript = document.getElementById("script-editor").value.trim();

    if (!editedScript) {
        alert("Please enter some script text before saving.");
        return;
    }

    const scriptContent = document.getElementById("script-content");
    scriptContent.replaceChildren();

    const scriptParagraph = document.createElement("p");
    scriptParagraph.textContent = editedScript;
    scriptContent.appendChild(scriptParagraph);

    alert("Edited script saved successfully!");
});


const saveToDatabaseButton = document.getElementById("save-to-database-btn");

saveToDatabaseButton.addEventListener("click", async function () {
    const editor = document.getElementById("script-editor");
    const content = editor.value.trim();

    if (!content) {
        alert("Please generate or enter a script first.");
        return;
    }

    const topic = document.getElementById("topic")?.value.trim() || "Untitled Topic";

    const title = topic + " - Saved Script";

    try {
        const response = await fetch("http://127.0.0.1:8000/api/saved-scripts/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                topic: topic,
                title: title,
                content: content
            })
        });

        if (!response.ok) {
            throw new Error("Unable to save script. Status: " + response.status);
        }
        await loadSavedScripts();
        alert("Script saved to database successfully!");
    } catch (error) {
        console.error("Save script error:", error);
        alert("Could not save the script. Make sure FastAPI is running.");
    }
});



const savedScriptsList = document.getElementById("saved-scripts-list");


const searchSavedScripts = document.getElementById("search-saved-scripts");
let allSavedScripts = [];

const sortSavedScripts = document.getElementById("sort-saved-scripts");

function filterAndSortSavedScripts() {
    const searchTerm = searchSavedScripts.value.trim().toLowerCase();
    const sortOrder = sortSavedScripts.value;

    const filteredScripts = allSavedScripts.filter(function (script) {
        return (
            script.title.toLowerCase().includes(searchTerm) ||
            script.topic.toLowerCase().includes(searchTerm)
        );
    });

    filteredScripts.sort(function (a, b) {
        const dateA = new Date(a.created_at).getTime();
        const dateB = new Date(b.created_at).getTime();

        if (sortOrder === "oldest") {
            return dateA - dateB;
        }

        return dateB - dateA;
    });

    displaySavedScripts(filteredScripts);
}

searchSavedScripts.addEventListener("input", filterAndSortSavedScripts);
sortSavedScripts.addEventListener("change", filterAndSortSavedScripts);


function displaySavedScripts(scripts) {
    savedScriptsList.replaceChildren();

    if (scripts.length === 0) {
        savedScriptsList.textContent = "No matching saved scripts found.";
        return;
    }

    scripts.forEach(function (script) {
        const item = document.createElement("div");
        item.className = "saved-script-item";

        const title = document.createElement("h3");
        title.textContent = script.title;

        const topic = document.createElement("p");
        topic.textContent = "Topic: " + script.topic;

        const reopenButton = document.createElement("button");
        reopenButton.type = "button";
        reopenButton.textContent = "Reopen Script";

        reopenButton.addEventListener("click", function () {
            document.getElementById("script-editor").value = script.content;

            document.getElementById("script-editor-container")
                .scrollIntoView({ behavior: "smooth" });
        });

        const updateButton = document.createElement("button");
        updateButton.type = "button";
        updateButton.textContent = "Update Saved Script";

        updateButton.addEventListener("click", async function () {
            const content = document.getElementById("script-editor").value.trim();

            if (!content) {
                alert("Please enter script content before updating.");
                return;
            }

            const updatedTopic =
                document.getElementById("topic")?.value.trim() || script.topic;

            const updatedTitle = updatedTopic + " - Saved Script";

            try {
                const response = await fetch(
                    `http://127.0.0.1:8000/api/saved-scripts/${script.id}`,
                    {
                        method: "PUT",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            topic: updatedTopic,
                            title: updatedTitle,
                            content: content
                        })
                    }
                );

                if (!response.ok) {
                    throw new Error("Unable to update saved script.");
                }

                await loadSavedScripts();
                alert("Saved script updated successfully!");
            } catch (error) {
                console.error("Update script error:", error);
                alert("Could not update the script. Please try again.");
            }
        });

        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.textContent = "Delete Script";

        deleteButton.addEventListener("click", async function () {
            if (!confirm("Are you sure you want to delete this saved script?")) {
                return;
            }

            try {
                const response = await fetch(
                    `http://127.0.0.1:8000/api/saved-scripts/${script.id}`,
                    { method: "DELETE" }
                );

                if (!response.ok) {
                    throw new Error("Failed to delete script.");
                }

                alert("Script deleted successfully!");
                await loadSavedScripts();
            } catch (error) {
                console.error("Delete script error:", error);
                alert("Could not delete the script. Please try again.");
            }
        });

        item.append(title, topic, reopenButton, updateButton, deleteButton);
        savedScriptsList.appendChild(item);
    });
}


async function loadSavedScripts() {
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/saved-scripts/"
        );

        if (!response.ok) {
            throw new Error("Failed to load saved scripts.");
        }

        const scripts = await response.json();
        allSavedScripts = scripts;
        displaySavedScripts(allSavedScripts);
    
        
    } catch (error) {
        console.error("Load saved scripts error:", error);
        savedScriptsList.textContent =
            "Unable to load saved scripts. Check that FastAPI is running.";
    }
}

loadSavedScripts();