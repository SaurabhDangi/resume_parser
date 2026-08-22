const analyzeBtn = document.getElementById("analyzeBtn");

analyzeBtn.addEventListener("click", async function () {

    const resumes = document.getElementById("resumes").files;
    const requirements =
        document.getElementById("requirements").value;

    const status =
        document.getElementById("status");

    // -----------------------------
    // Validate input
    // -----------------------------

    if (resumes.length === 0) {
        status.textContent = "Please select at least one resume.";
        return;
    }

    if (!requirements.trim()) {
        status.textContent = "Please enter HR requirements.";
        return;
    }

    // -----------------------------
    // Show selected files
    // -----------------------------

    console.log("Number of resumes:", resumes.length);

    for (let i = 0; i < resumes.length; i++) {
        console.log("Resume:", resumes[i].name);
    }

    status.textContent = "Analyzing resumes...";

    // -----------------------------
    // Create FormData
    // -----------------------------

    const formData = new FormData();

    // Add every resume
    for (let i = 0; i < resumes.length; i++) {
        formData.append("files", resumes[i]);
    }

    // Add HR requirements
    formData.append(
        "hr_requirements",
        requirements
    );

    // -----------------------------
    // Send request to FastAPI
    // -----------------------------

    try {

        const response = await fetch(
            "https://resume-parser-nod7.onrender.com/rank-resumes",
            {
                method: "POST",
                body: formData
            }
        );

        console.log("HTTP status:", response.status);

        if (!response.ok) {

            const errorText = await response.text();

            throw new Error(
                `Server error ${response.status}: ${errorText}`
            );
        }

        // -----------------------------
        // Read JSON response
        // -----------------------------

        const data = await response.json();

        console.log("Ranking result:", data);

        // -----------------------------
        // Display result
        // -----------------------------

        status.textContent = "Analysis complete!";

        console.log(
            "Total candidates:",
            data.total_candidates
        );

        console.log(
            "Rankings:",
            data.rankings
        );

        // For now, show rankings in the page
        const result = document.getElementById("result");

        result.classList.remove("hidden");

        let html = "<h2>Rankings</h2>";

        data.rankings.forEach(function (candidate) {

            html += `
                <div class="candidate">

                    <h3>
                        #${candidate.rank}
                        ${candidate.filename}
                    </h3>

                    <p>
                        Match:
                        <strong>
                            ${candidate.match_percentage}%
                        </strong>
                    </p>

                    <p>
                        Skills:
                        ${candidate.skills_match}%
                    </p>

                    <p>
                        Experience:
                        ${candidate.experience_match}%
                    </p>

                    <p>
                        Projects:
                        ${candidate.projects_match}%
                    </p>

                    <p>
                        Education:
                        ${candidate.education_match}%
                    </p>

                    <p>
                        <strong>Skills Found:</strong>
                        ${candidate.skills_found.join(", ")}
                    </p>

                    <p>
                        <strong>Skills Missing:</strong>
                        ${candidate.skills_missing.join(", ")}
                    </p>

                    <p>
                        <strong>Summary:</strong>
                        ${candidate.summary}
                    </p>

                </div>
            `;

        });

        result.innerHTML = html;

    } catch (error) {

        console.error("ERROR:", error);

        status.textContent =
            "Something went wrong: " + error.message;
    }

});