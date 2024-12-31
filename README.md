


# Documentation for front matter of marble markdown files


### **YAML Front Matter Pieces to Add**

1. **`date_created`**
    
    - **Default Value:** `YYYY-MM-DD` (from the CSV).
    - **Behavior:**
        - If the value is `YYYY-MM-DD`, display in HTML as `Created on: YYYY-MM-DD`.
        - If the value is `YYYY-MM-DD, Custom Text`, display in HTML with the custom text (e.g., `Posted on: YYYY-MM-DD`).
2. **`date_lastchanged`**
    
    - **Default Value:** `YYYY-MM-DD` (from the CSV).
    - **Behavior:**
        - If the value is `YYYY-MM-DD`, display in HTML as `Last updated: YYYY-MM-DD`.
        - If the value is `YYYY-MM-DD, Custom Text`, display in HTML with the custom text (e.g., `Reviewed on: YYYY-MM-DD`).
3. **`show_update_lastchanged`**
    
    - **Default Value:** `NO, NO`.
    - **Behavior:**
        - **First Value (`NO` or `YES`):** Determines if `date_lastchanged` is displayed in the HTML.
            - `NO`: Do not show `date_lastchanged` in the HTML.
            - `YES`: Show `date_lastchanged` in the HTML using the specified custom text or default formatting.
        - **Second Value (`NO` or `YES`):** Determines if the script should automatically update the `date_lastchanged` field based on changes to the markdown file.
            - `NO`: Do not update the `date_lastchanged` value automatically.
            - `YES`: Automatically update the `date_lastchanged` value when changes are detected in the markdown file.
