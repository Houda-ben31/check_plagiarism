// زر الفحص
document.getElementById("checkButton").addEventListener("click", async function() {
    const text = document.getElementById("mycontent").value;

    if (!text.trim()) {
        alert("Please enter text to check!");
        return;
    }

    // إظهار شريط التحميل
    document.getElementById("percent").innerText = "Checking...";
    document.querySelector(".percentimg").style.display = "block";

    try {
        // إرسال النص إلى Python API
        const response = await fetch("http://127.0.0.1:8000/api/check", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content: text })
        });

        const result = await response.json();

        // إخفاء شريط التحميل
        document.querySelector(".percentimg").style.display = "none";

        // عرض نسبة الانتحال
        document.getElementById("percent").innerText =
            "Plagiarism Detected: " + result.percent + "%";

        // عرض جدول النتائج
        document.getElementById("resultList").innerHTML = result.table_html;

        // **اختياري**: تلوين النسبة بناءً على القيمة
        if(result.percent > 70) {
            document.getElementById("percent").style.color = "red";
        } else if(result.percent > 30) {
            document.getElementById("percent").style.color = "orange";
        } else {
            document.getElementById("percent").style.color = "green";
        }

    } catch (error) {
        console.error("Error:", error);
        alert("There was an error connecting to the API.");
        document.querySelector(".percentimg").style.display = "none";
    }
});

// تحديث عداد الكلمات
const textarea = document.getElementById("mycontent");
const wordCountSpan = document.getElementById("words-count");
const maxWords = 2000;

textarea.addEventListener("input", () => {
    const words = textarea.value.trim().split(/\s+/).filter(w => w.length > 0);
    wordCountSpan.innerText = words.length;

    if (words.length > maxWords) {
        textarea.value = words.slice(0, maxWords).join(" ");
        wordCountSpan.innerText = maxWords;
        alert("Maximum word limit reached!");
    }
});
