import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import ctypes
import uuid
import os


# =============================================================================
# SYSTEM ARCHITECT : Expert Nosrat Jahan
# PROJECT NAME     : CircleUp Professional Social Suite
# RELEASE VERSION  : 4.0.0 (Enterprise Stable)
# CORE FRAMEWORK   : Python Tkinter / Pillow / Windows High-DPI API
# =============================================================================

class CircleUpApp:
    """Main Application Controller for CircleUp Pro."""

    def __init__(self, root):
        self.root = root
        self.root.title("CircleUp Pro v4.0.0 | Enterprise Suite")
        self.root.geometry("1400x900")
        self.root.configure(bg="#F0F2F5")

        # --- System Palette ---
        self.THEME_BLUE = "#1877F2"
        self.THEME_GREEN = "#42B72A"
        self.BG_LIGHT = "#F0F2F5"
        self.BORDER_COLOR = "#DDDFE2"

        # --- State Management ---
        self.asset_registry = {}  # Object pool for Image references
        self.selected_image_path = None
        self.current_user = "Expert User"

        # --- Initialization ---
        self._set_dpi_awareness()
        self._initialize_context_menu()
        self._render_authentication_gate()

    def _set_dpi_awareness(self):
        """Enables High-DPI Scaling for crisp typography and UI elements."""
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    def _initialize_context_menu(self):
        """Builds a global context menu for Cut, Copy, and Paste operations."""
        self.ctx_menu = tk.Menu(self.root, tearoff=0)
        self.ctx_menu.add_command(label="Cut", command=lambda: self.focus_widget.event_generate("<<Cut>>"))
        self.ctx_menu.add_command(label="Copy", command=lambda: self.focus_widget.event_generate("<<Copy>>"))
        self.ctx_menu.add_command(label="Paste", command=lambda: self.focus_widget.event_generate("<<Paste>>"))
        self.focus_widget = None

    def _show_context_menu(self, event):
        self.focus_widget = event.widget
        self.ctx_menu.post(event.x_root, event.y_root)

    # -------------------------------------------------------------------------
    # AUTHENTICATION COMPONENTS
    # -------------------------------------------------------------------------
    def _render_authentication_gate(self):
        """Constructs the primary Login Gateway."""
        self.auth_frame = tk.Frame(self.root, bg="#FFFFFF", padx=80, pady=70, bd=1, relief="flat", highlightthickness=1,
                                   highlightbackground=self.BORDER_COLOR)
        self.auth_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Corporate Branding
        try:
            logo_img = Image.open("wolf.png").resize((130, 130), Image.Resampling.LANCZOS)
            self.asset_registry['login_logo'] = ImageTk.PhotoImage(logo_img)
            tk.Label(self.auth_frame, image=self.asset_registry['login_logo'], bg="#FFFFFF").pack(pady=(0, 15))
        except:
            tk.Label(self.auth_frame, text="🐺", font=("Segoe UI", 60), bg="#FFFFFF").pack()

        tk.Label(self.auth_frame, text="CircleUp", font=("Segoe UI", 42, "bold"), fg=self.THEME_BLUE,
                 bg="#FFFFFF").pack()
        tk.Label(self.auth_frame, text="Connect with your professional network.", font=("Segoe UI", 12), fg="#65676B",
                 bg="#FFFFFF").pack(pady=(0, 45))

        # Authentication Inputs
        self.user_id_entry = self._create_form_input(self.auth_frame, "Email or Phone Number", 35)
        self.user_id_entry.bind("<Return>", lambda e: self._launch_main_dashboard())

        tk.Button(self.auth_frame, text="Log In", font=("Segoe UI", 14, "bold"), bg=self.THEME_BLUE, fg="white",
                  bd=0, width=32, cursor="hand2", command=self._launch_main_dashboard).pack(pady=(25, 10), ipady=15)

        tk.Frame(self.auth_frame, bg=self.BORDER_COLOR, height=1, width=350).pack(pady=20)

        tk.Button(self.auth_frame, text="Create New Account", font=("Segoe UI", 14, "bold"), bg=self.THEME_GREEN,
                  fg="white",
                  bd=0, width=28, cursor="hand2", command=self._spawn_registration_modal).pack(ipady=15)

    def _create_form_input(self, parent, placeholder, width, secret=False):
        """Factory method for creating standardized inputs with auto-placeholder logic."""
        entry = ttk.Entry(parent, width=width, font=("Segoe UI", 12), foreground="grey")
        entry.insert(0, placeholder)

        def on_focus_in(e):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.configure(foreground="black")
                if secret: entry.configure(show="*")

        def on_focus_out(e):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.configure(foreground="grey")
                if secret: entry.configure(show="")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        entry.bind("<Button-3>", self._show_context_menu)
        entry.pack(pady=10, ipady=12)
        return entry

    def _spawn_registration_modal(self):
        """Initializes a modal window for user registration."""
        modal = tk.Toplevel(self.root)
        modal.title("Create CircleUp Account")
        modal.geometry("500x720")
        modal.configure(bg="#FFFFFF")
        modal.grab_set()

        header = tk.Frame(modal, bg="#FFFFFF", pady=25)
        header.pack(fill="x")
        tk.Label(header, text="Sign Up", font=("Segoe UI", 28, "bold"), bg="#FFFFFF").pack()
        tk.Label(header, text="It's quick and easy.", font=("Segoe UI", 11), fg="#65676B", bg="#FFFFFF").pack()

        # Input Sequential Navigation
        fn = self._create_form_input(modal, "First Name", 40)
        ln = self._create_form_input(modal, "Last Name", 40)
        em = self._create_form_input(modal, "Mobile number or email", 40)
        pw = self._create_form_input(modal, "New Password", 40, secret=True)

        fn.bind("<Return>", lambda e: ln.focus_set())
        ln.bind("<Return>", lambda e: em.focus_set())
        em.bind("<Return>", lambda e: pw.focus_set())
        pw.bind("<Return>", lambda e: [modal.destroy(), self._launch_main_dashboard()])

        tk.Button(modal, text="Sign Up", font=("Segoe UI", 14, "bold"), bg=self.THEME_GREEN, fg="white",
                  bd=0, width=22, command=lambda: [modal.destroy(), self._launch_main_dashboard()]).pack(pady=35,
                                                                                                         ipady=13)

    # -------------------------------------------------------------------------
    # MAIN APPLICATION ENGINE
    # -------------------------------------------------------------------------
    def _launch_main_dashboard(self):
        """Transition from Auth to Main Dashboard."""
        self.auth_frame.destroy()

        # Navigation System
        nav = tk.Frame(self.root, bg="#FFFFFF", height=65, bd=0, highlightthickness=1,
                       highlightbackground=self.BORDER_COLOR)
        nav.pack(fill="x", side="top")
        tk.Label(nav, text="CircleUp", font=("Segoe UI", 22, "bold"), fg=self.THEME_BLUE, bg="#FFFFFF").pack(
            side="left", padx=45)

        # 3-Column Workspace Architecture
        self.main_container = tk.Frame(self.root, bg=self.BG_LIGHT)
        self.main_container.pack(fill="both", expand=True)

        self._build_sidebar_dashboard()
        self._build_contact_sidebar()
        self._initialize_news_feed()

    def _build_sidebar_dashboard(self):
        """Constructs the Navigation Dashboard on the left."""
        left_col = tk.Frame(self.main_container, bg=self.BG_LIGHT, width=320)
        left_col.pack(side="left", fill="y", padx=20, pady=25)
        left_col.pack_propagate(False)

        tk.Label(left_col, text=f"👤  {self.current_user}", font=("Segoe UI", 12, "bold"), bg=self.BG_LIGHT,
                 anchor="w").pack(fill="x", padx=20, pady=12)

        nav_links = [("👥 Friends"), ("🏠 Groups"), ("🛍️ Marketplace"), ("🕒 Memories"), ("🔖 Saved")]
        for link_text in nav_links:
            tk.Button(left_col, text=link_text, font=("Segoe UI", 11), bg=self.BG_LIGHT, bd=0, anchor="w", padx=20,
                      pady=12, cursor="hand2").pack(fill="x")

        # System Architect Branding (Enhanced Visuals)
        credit_box = tk.Frame(left_col, bg="#FFFFFF", highlightthickness=1, highlightbackground=self.THEME_BLUE,
                              padx=20, pady=22)
        credit_box.pack(side="bottom", fill="x", padx=15, pady=35)

        tk.Label(credit_box, text="SYSTEM ARCHITECT", font=("Segoe UI", 8, "bold"), fg=self.THEME_BLUE,
                 bg="#FFFFFF").pack(anchor="w")
        tk.Label(credit_box, text="Expert Nosrat Jahan", font=("Segoe UI", 14, "bold"), fg="#050505",
                 bg="#FFFFFF").pack(anchor="w", pady=(2, 0))
        tk.Frame(credit_box, bg=self.THEME_BLUE, height=2, width=45).pack(anchor="w", pady=10)
        tk.Label(credit_box, text="© 2026 CircleUp Social Lab", font=("Segoe UI", 8), fg="#65676B", bg="#FFFFFF").pack(
            anchor="w")

    def _build_contact_sidebar(self):
        """Renders the Contact List on the right."""
        right_col = tk.Frame(self.main_container, bg=self.BG_LIGHT, width=320)
        right_col.pack(side="right", fill="y", padx=20, pady=25)

        tk.Label(right_col, text="Contacts", font=("Segoe UI", 13, "bold"), fg="#65676B", bg=self.BG_LIGHT).pack(
            anchor="w", padx=20, pady=12)

        directory = ["Mushfiq Mahim", "Sabbir Ahmed", "Meta Global AI", "Antik Mahmud"]
        for contact_name in directory:
            row = tk.Frame(right_col, bg=self.BG_LIGHT, pady=8)
            row.pack(fill="x", padx=20)
            tk.Label(row, text="●", fg=self.THEME_GREEN, bg=self.BG_LIGHT).pack(side="left")
            tk.Label(row, text=contact_name, font=("Segoe UI", 10), bg=self.BG_LIGHT).pack(side="left", padx=12)

    def _initialize_news_feed(self):
        """Initializes the centralized, scrollable Feed Hub."""
        center_col = tk.Frame(self.main_container, bg=self.BG_LIGHT)
        center_col.pack(side="left", fill="both", expand=True)

        canvas = tk.Canvas(center_col, bg=self.BG_LIGHT, highlightthickness=0)
        v_bar = ttk.Scrollbar(center_col, orient="vertical", command=canvas.yview)
        self.feed_hub = tk.Frame(canvas, bg=self.BG_LIGHT)

        self.feed_hub.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        feed_win = canvas.create_window((350, 0), window=self.feed_hub, anchor="n")
        canvas.configure(yscrollcommand=v_bar.set)

        canvas.pack(side="left", fill="both", expand=True)
        v_bar.pack(side="right", fill="y")

        canvas.bind('<Configure>', lambda e: canvas.itemconfig(feed_win, width=min(e.width, 700)))

        self._build_post_composer()

    def _build_post_composer(self):
        """Renders the interactive Post Creator."""
        composer_card = tk.Frame(self.feed_hub, bg="#FFFFFF", padx=25, pady=25, highlightthickness=1,
                                 highlightbackground=self.BORDER_COLOR)
        composer_card.pack(pady=25, fill="x", padx=20)

        self.post_input_area = tk.Text(composer_card, font=("Segoe UI", 13), height=3, bg="#F0F2F5", bd=0, padx=15,
                                       pady=15)
        self.post_input_area.bind("<Button-3>", self._show_context_menu)
        self.post_input_area.pack(fill="x", pady=(0, 20))

        action_bar = tk.Frame(composer_card, bg="#FFFFFF")
        action_bar.pack(fill="x")

        tk.Button(action_bar, text="📷 Photo/Video", font=("Segoe UI", 11, "bold"), bg="#F2F3F5", bd=0, padx=20,
                  cursor="hand2", command=self._trigger_media_picker).pack(side="left")
        tk.Button(action_bar, text="Post", font=("Segoe UI", 11, "bold"), bg=self.THEME_BLUE, fg="white", bd=0, padx=50,
                  cursor="hand2", command=self._handle_post_submission).pack(side="right")

    def _trigger_media_picker(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if path:
            self.selected_image_path = path
            messagebox.showinfo("Asset Attached", f"Target: {os.path.basename(path)}")

    def _handle_post_submission(self):
        content = self.post_input_area.get("1.0", "end-1c").strip()
        if content or self.selected_image_path:
            self._deploy_post_card(content, self.selected_image_path)
            self.post_input_area.delete("1.0", tk.END)
            self.selected_image_path = None
        else:
            messagebox.showwarning("System Notification", "Required: Post content cannot be empty.")

    def _deploy_post_card(self, text, image_path):
        """Deploys a new Social Card into the News Feed Hub."""
        card = tk.Frame(self.feed_hub, bg="#FFFFFF", padx=25, pady=25, highlightthickness=1,
                        highlightbackground=self.BORDER_COLOR)
        card.pack(pady=12, fill="x", padx=20)

        tk.Label(card, text=self.current_user, font=("Segoe UI", 12, "bold"), bg="#FFFFFF").pack(anchor="w")

        if text:
            tk.Label(card, text=text, font=("Segoe UI", 13), bg="#FFFFFF", wraplength=600, justify="left").pack(
                anchor="w", pady=15)

        if image_path:
            try:
                processed_img = Image.open(image_path)
                processed_img.thumbnail((600, 450))
                final_asset = ImageTk.PhotoImage(processed_img)
                self.asset_registry[str(uuid.uuid4())] = final_asset  # Persistent registry
                tk.Label(card, image=final_asset, bg="#FFFFFF").pack(pady=10)
            except:
                pass

        # Interaction Module
        interaction_layer = tk.Frame(card, bg="#FFFFFF", pady=15)
        interaction_layer.pack(fill="x")

        # Like Hook
        like_hook = tk.Button(interaction_layer, text="👍 Like", font=("Segoe UI", 11, "bold"), fg="#65676B",
                              bg="#FFFFFF", bd=0, cursor="hand2")
        like_hook.pack(side="left", expand=True)
        like_hook.config(command=lambda: like_hook.config(fg=self.THEME_BLUE))

        # Comment Hook
        tk.Button(interaction_layer, text="💬 Comment", font=("Segoe UI", 11, "bold"), fg="#65676B", bg="#FFFFFF", bd=0,
                  cursor="hand2", command=lambda: self._spawn_comment_dialog(card)).pack(side="left", expand=True)

        # Share Hook
        tk.Button(interaction_layer, text="🔄 Share", font=("Segoe UI", 11, "bold"), fg="#65676B", bg="#FFFFFF", bd=0,
                  cursor="hand2",
                  command=lambda: messagebox.showinfo("Broadcast", "Successfully shared to timeline.")).pack(
            side="left", expand=True)

    def _spawn_comment_dialog(self, target_card):
        dialog = tk.Toplevel(self.root)
        dialog.title("Submit Comment")
        dialog.geometry("400x180")

        input_f = ttk.Entry(dialog, width=38)
        input_f.pack(pady=35, ipady=12)
        input_f.bind("<Return>", lambda e: commit())

        def commit():
            if input_f.get():
                tk.Label(target_card, text=f"🗨️ {input_f.get()}", font=("Segoe UI", 10), bg="#F2F3F5", anchor="w",
                         padx=15, pady=8).pack(fill="x", pady=4)
                dialog.destroy()

        tk.Button(dialog, text="Submit", bg=self.THEME_BLUE, fg="white", command=commit).pack()


if __name__ == "__main__":
    main_window = tk.Tk()
    application = CircleUpApp(main_window)
    main_window.mainloop()