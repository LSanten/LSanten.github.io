---
date_created: '2025-01-10'
date_lastchanged: '2025-01-10'
layout: default
show_date_lastchanged_updatedauto: YES, NO, NO
---
### **How to Add "Copy Path (No Quotes)" to the Context Menu in Windows**

#### **Step 1: Open the Registry Editor**

1. Press **Win + R** to open the Run dialog.
2. Type `regedit` and press **Enter** or click **OK**.
3. If prompted by User Account Control (UAC), click **Yes** to allow changes.

---

#### **Step 2: Navigate to the Key**

1. In the Registry Editor, go to:
    `HKEY_CLASSES_ROOT\AllFilesystemObjects\shell`
    - Expand the folders in the left-hand tree view to navigate to the `shell` folder.

---

#### **Step 3: Create the "CopyPathNoQuotes" Key**

1. Right-click the **shell** folder.
2. Select **New > Key**.
3. Name the new key:
	`CopyPathNoQuotes`

---

#### **Step 4: Set the Display Name**

1. Select the `CopyPathNoQuotes` key.
2. In the right-hand pane, double-click the **(Default)** entry.
3. Set the value to:
    `Copy Path (No Quotes)`
4. Click **OK** to save.

---

#### **Step 5: Create the "command" Subkey**

1. Right-click the `CopyPathNoQuotes` key.
2. Select **New > Key**.
3. Name the new key:
    `command`

---

#### **Step 6: Set the Command**

1. Select the `command` key.
2. In the right-hand pane, double-click the **(Default)** entry.
3. Set the value to:
    `cmd.exe /c echo %1 | clip`
4. Click **OK** to save.

---

### **Final Registry Structure**

Your registry should now look like this:
```
HKEY_CLASSES_ROOT  
└─ AllFilesystemObjects    
	└─ shell
	        └─ CopyPathNoQuotes
	                   └─ command

````

---

#### **Step 7: Close the Registry Editor**

1. Click **File > Exit** to close the Registry Editor.
    - This ensures that the Registry Editor doesn't open inadvertently when using the new context menu option.