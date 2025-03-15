document.getElementById("saveButton").addEventListener("click", async () => {
    // Get data from the popup fields
    const title = document.getElementById("title").value;
    const price = parseFloat(document.getElementById("price").value) || 0;
  
    // Get the current tab URL
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const url = tab.url;
  
    // We'll skip "image_url" for now or set an empty string
    const image_url = "";
  
    // Send POST request to the FastAPI endpoint
    const backendUrl = "http://127.0.0.1:8000/api/wishlist";
  
    try {
      const res = await fetch(backendUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title,
          url,
          price,
          image_url
        })
      });
  
      const data = await res.json();
      console.log("Response from API:", data);
      alert("Item saved to wishlist!");
    } catch (err) {
      console.error("Error saving item:", err);
      alert("Failed to save item. Check console for errors.");
    }
  });
  