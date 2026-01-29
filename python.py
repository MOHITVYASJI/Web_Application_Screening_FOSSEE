import os

# Target directory
base_path = r"E:\FOSSEE\Web_Application_Screening_FOSSEE\frontend\src\components\ui"

# List of UI component files
files = [
    "accordion.jsx",
    "alert-dialog.jsx",
    "alert.jsx",
    "aspect-ratio.jsx",
    "avatar.jsx",
    "badge.jsx",
    "breadcrumb.jsx",
    "button.jsx",
    "calendar.jsx",
    "card.jsx",
    "carousel.jsx",
    "checkbox.jsx",
    "collapsible.jsx",
    "command.jsx",
    "context-menu.jsx",
    "dialog.jsx",
    "drawer.jsx",
    "dropdown-menu.jsx",
    "form.jsx",
    "hover-card.jsx",
    "input-otp.jsx",
    "input.jsx",
    "label.jsx",
    "menubar.jsx",
    "navigation-menu.jsx",
    "pagination.jsx",
    "popover.jsx",
    "progress.jsx",
    "radio-group.jsx",
    "resizable.jsx",
    "scroll-area.jsx",
    "select.jsx",
    "separator.jsx",
    "sheet.jsx",
    "skeleton.jsx",
    "slider.jsx",
    "sonner.jsx",
    "switch.jsx",
    "table.jsx",
    "tabs.jsx",
    "textarea.jsx",
    "toast.jsx",
    "toaster.jsx",
    "toggle-group.jsx",
    "toggle.jsx",
    "tooltip.jsx"
]

# Create directory if not exists
os.makedirs(base_path, exist_ok=True)

# Create files
for file in files:
    file_path = os.path.join(base_path, file)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"// {file}\n")
            f.write("// Auto-generated UI component file\n\n")
        print(f"Created: {file}")
    else:
        print(f"Already exists: {file}")

print("\n✅ All UI component files are ready!")
