import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import backend

# Login Window Class
class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("Admin Login")
        self.root.geometry("400x300")
        self.root.configure(bg="#331438")
        
        # Styling
        self.style = ttk.Style()
        self.style.configure("TLabel", background="#dbe2e9", font=("Arial", 12))
        self.style.configure("TButton", font=("Arial", 11))
        self.style.configure("TEntry", font=("Arial", 11))
        
        # Login Frame
        self.frame = ttk.Frame(self.root, padding="20", style="Custom.TFrame")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        ttk.Label(self.frame, text="Smart Inventory System", 
                 font=("Arial", 16, "bold"), foreground="#2c3e50").pack(pady=10)
        
        # Username
        ttk.Label(self.frame, text="Username").pack()
        self.username = ttk.Entry(self.frame)
        self.username.pack(pady=5, fill="x")
        
        # Password
        ttk.Label(self.frame, text="Password").pack()
        self.password = ttk.Entry(self.frame, show="*")
        self.password.pack(pady=5, fill="x")
        
        # Login Button
        ttk.Button(self.frame, text="Login", command=self.validate_login,
                  style="Accent.TButton").pack(pady=20)
        
        # Configure styles
        self.style.configure("Custom.TFrame", background="#3b0f3f")
        self.style.configure("Accent.TButton", background="#161718", 
                           foreground="black", padding=10)
        
        # Center window
        self.root.update()
        self.root.minsize(400, 300)

    def validate_login(self):
        username = self.username.get()
        password = self.password.get()
        
        if backend.validate_admin(username, password):
            self.root.destroy()
            self.on_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

# Main Application Class
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Inventory Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#2e3030")
        
        # Initialize Database
        backend.init_db()
        
        # Styling
        self.style = ttk.Style()
        self.style.configure("TLabel", background="#202223", font=("Arial", 11))
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("Treeview", font=("Arial", 10))
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"),
                           background="#d5d3ee", foreground="black")
        self.style.configure("Back.TButton", background="#3c1a3f", 
                           foreground="black", padding=10, font=("Arial", 8, "bold"))
        # Button styles for home page
        self.style.configure("Inventory.TButton", background="#BFFA9F", 
                           foreground="black", padding=15, font=("Arial", 14, "bold"))
        self.style.configure("Orders.TButton", background="#2196F3", 
                           foreground="black", padding=15, font=("Arial", 14, "bold"))
        self.style.configure("Suppliers.TButton", background="#FFC107", 
                           foreground="black", padding=15, font=("Arial", 14, "bold"))
        self.style.configure("Customers.TButton", background="#E91E63", 
                           foreground="black", padding=15, font=("Arial", 14, "bold"))
        self.style.configure("Reports.TButton", background="#9C27B0", 
                           foreground="black", padding=15, font=("Arial", 14, "bold"))
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)
        
        # Create top frame for back button
        self.top_frame = ttk.Frame(self.main_container, style="Tab.TFrame")
        self.top_frame.pack(fill="x")
        
        # Back to Home Button (shown when tabs are active)
        self.back_button = ttk.Button(self.top_frame, text="← Back to Home",
                                    command=self.show_home, style="Back.TButton")
        
        # Create Home Page Frame
        self.home_frame = ttk.Frame(self.main_container, style="Tab.TFrame")
        self.home_frame.pack(fill="both", expand=True)
        
        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(self.main_container, style="Tab.TFrame")
        # Notebook is not packed initially; it will be shown when a tab is selected
        
        # Frames for Tabs
        self.inventory_frame = ttk.Frame(self.notebook, style="Tab.TFrame")
        self.order_frame = ttk.Frame(self.notebook, style="Tab.TFrame")
        self.supplier_frame = ttk.Frame(self.notebook, style="Tab.TFrame")
        self.customer_frame = ttk.Frame(self.notebook, style="Tab.TFrame")
        self.report_frame = ttk.Frame(self.notebook, style="Tab.TFrame")
        
        self.notebook.add(self.inventory_frame, text="Inventory")
        self.notebook.add(self.order_frame, text="Orders")
        self.notebook.add(self.supplier_frame, text="Suppliers")
        self.notebook.add(self.customer_frame, text="Customers")
        self.notebook.add(self.report_frame, text="Reports")
        
        # Configure frame style
        self.style.configure("Tab.TFrame", background="#d2a9dd")
        
        # Setup Home Page
        self.setup_home_page()
        
        # Setup UI for Each Tab
        self.setup_inventory_tab()
        self.setup_order_tab()
        self.setup_supplier_tab()
        self.setup_customer_tab()
        self.setup_report_tab()
        
        # Check for restock alerts on startup
        self.check_restock_alerts()

    def setup_home_page(self):
        # Main content frame for centering
        content_frame = ttk.Frame(self.home_frame, style="Tab.TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Welcome Message
        tk.Label(content_frame, text="Welcome to Smart Inventory Management System",
                font=("Arial", 18, "bold"), bg="#d2a9dd", fg="#2c3e50").pack(pady=20)
        
        # Button Frame for centered buttons
        button_frame = ttk.Frame(content_frame, style="Tab.TFrame")
        button_frame.pack(pady=10)
        
        # Centered Buttons
        ttk.Button(button_frame, text="Inventory", command=lambda: self.show_tab(0),
                  style="Inventory.TButton").pack(fill="x", pady=10, padx=50)
        ttk.Button(button_frame, text="Orders", command=lambda: self.show_tab(1),
                  style="Orders.TButton").pack(fill="x", pady=10, padx=50)
        ttk.Button(button_frame, text="Suppliers", command=lambda: self.show_tab(2),
                  style="Suppliers.TButton").pack(fill="x", pady=10, padx=50)
        ttk.Button(button_frame, text="Customers", command=lambda: self.show_tab(3),
                  style="Customers.TButton").pack(fill="x", pady=10, padx=50)
        ttk.Button(button_frame, text="Reports", command=lambda: self.show_tab(4),
                  style="Reports.TButton").pack(fill="x", pady=10, padx=50)

    def show_tab(self, tab_index):
        # Hide home frame, show top frame with back button and notebook
        self.home_frame.pack_forget()
        self.top_frame.pack(fill="x")
        self.back_button.pack(side="left", padx=15, pady=10)
        self.notebook.pack(fill="both", expand=True)
        self.notebook.select(tab_index)

    def show_home(self):
        # Hide notebook and top frame, show home frame
        self.notebook.pack_forget()
        self.top_frame.pack_forget()
        self.back_button.pack_forget()
        self.home_frame.pack(fill="both", expand=True)

    # Inventory Tab
    def setup_inventory_tab(self):
        tk.Label(self.inventory_frame, text="Inventory Management",
                font=("Arial", 14, "bold"), bg="#f0f5f7", fg="#8752f0").pack(pady=10)
        
        # Entry Fields Frame
        entry_frame = ttk.Frame(self.inventory_frame, padding="10", style="Tab.TFrame")
        entry_frame.pack(fill="x")
        
        tk.Label(entry_frame, text="Product Name", bg="#c9dceb").pack()
        self.product_name = ttk.Entry(entry_frame)
        self.product_name.pack(pady=5, fill="x")
        
        tk.Label(entry_frame, text="Stock Level", bg="#d8ebf8").pack()
        self.stock_level = ttk.Entry(entry_frame)
        self.stock_level.pack(pady=5, fill="x")
        
        tk.Label(entry_frame, text="Restock Threshold", bg="#e4f6fa").pack()
        self.restock_threshold = ttk.Entry(entry_frame)
        self.restock_threshold.pack(pady=5, fill="x")
        
        # Buttons
        ttk.Button(entry_frame, text="Add/Restock Product", command=self.add_product,
                  style="Accent.TButton").pack(pady=5)
        ttk.Button(entry_frame, text="Update Product", command=self.update_product,
                  style="Accent.TButton").pack(pady=5)
        ttk.Button(entry_frame, text="Delete Product", command=self.delete_product,
                  style="Accent.TButton").pack(pady=5)
        
        # Inventory Treeview
        self.inventory_tree = ttk.Treeview(self.inventory_frame, 
                                        columns=("ID", "Name", "Stock", "Threshold"), 
                                        show="headings")
        self.inventory_tree.heading("ID", text="ID")
        self.inventory_tree.heading("Name", text="Name")
        self.inventory_tree.heading("Stock", text="Stock Level")
        self.inventory_tree.heading("Threshold", text="Restock Threshold")
        self.inventory_tree.pack(pady=10, fill="both", expand=True)
        self.inventory_tree.bind('<<TreeviewSelect>>', self.load_product)
        
        self.load_inventory()

    def add_product(self):
        name = self.product_name.get()
        stock = self.stock_level.get()
        threshold = self.restock_threshold.get()
        
        if name and stock.isdigit() and threshold.isdigit():
            backend.add_product(name, stock, threshold)
            self.load_inventory()
            self.check_restock_alerts()
            self.clear_inventory_fields()
        else:
            messagebox.showerror("Error", "Please enter valid details")

    def update_product(self):
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a product to update")
            return
        
        item = self.inventory_tree.item(selected)
        product_id = item['values'][0]
        name = self.product_name.get()
        stock = self.stock_level.get()
        threshold = self.restock_threshold.get()
        
        if name and stock.isdigit() and threshold.isdigit():
            backend.update_product(product_id, name, stock, threshold)
            self.load_inventory()
            self.check_restock_alerts()
            self.clear_inventory_fields()
        else:
            messagebox.showerror("Error", "Please enter valid details")

    def delete_product(self):
        selected = self.inventory_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a product to delete")
            return
        
        item = self.inventory_tree.item(selected)
        product_id = item['values'][0]
        
        success, message = backend.delete_product(product_id)
        if success:
            messagebox.showinfo("Success", message)
            self.load_inventory()
            self.check_restock_alerts()
            self.clear_inventory_fields()
        else:
            messagebox.showerror("Error", message)

    def load_product(self, event):
        selected = self.inventory_tree.selection()
        if selected:
            item = self.inventory_tree.item(selected)
            self.product_name.delete(0, tk.END)
            self.stock_level.delete(0, tk.END)
            self.restock_threshold.delete(0, tk.END)
            self.product_name.insert(0, item['values'][1])
            self.stock_level.insert(0, item['values'][2])
            self.restock_threshold.insert(0, item['values'][3])

    def clear_inventory_fields(self):
        self.product_name.delete(0, tk.END)
        self.stock_level.delete(0, tk.END)
        self.restock_threshold.delete(0, tk.END)

    def load_inventory(self):
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        for row in backend.load_inventory():
            self.inventory_tree.insert("", tk.END, values=row)

    def check_restock_alerts(self):
        low_stock = backend.check_restock_alerts()
        if low_stock:
            alert_msg = "Low Stock Alert:\n"
            for product in low_stock:
                alert_msg += f"{product[0]}: {product[1]} units (Threshold: {product[2]})\n"
            messagebox.showwarning("Restock Alert", alert_msg)

    # Order Tab
    def setup_order_tab(self):
        tk.Label(self.order_frame, text="Order Management",
                font=("Arial", 14, "bold"), bg="#e7ebec", fg="#6c29ab").pack(pady=10)
        
        entry_frame = ttk.Frame(self.order_frame, padding="10", style="Tab.TFrame")
        entry_frame.pack(fill="x")
        
        tk.Label(entry_frame, text="Customer ID", bg="#f7fbfc").pack()
        self.order_customer_id = ttk.Entry(entry_frame)
        self.order_customer_id.pack(pady=5, fill="x")
        
        tk.Label(entry_frame, text="Product ID", bg="#eef4f5").pack()
        self.order_product_id = ttk.Entry(entry_frame)
        self.order_product_id.pack(pady=5, fill="x")
        
        tk.Label(entry_frame, text="Quantity", bg="#dfebee").pack()
        self.order_quantity = ttk.Entry(entry_frame)
        self.order_quantity.pack(pady=5, fill="x")
        
        tk.Label(entry_frame, text="Order Status", bg="#e0e9eb").pack()
        self.order_status = ttk.Entry(entry_frame)
        self.order_status.pack(pady=5, fill="x")
        
        ttk.Button(entry_frame, text="Place Order", command=self.place_order,
                  style="Accent.TButton").pack(pady=5)
        
        self.order_tree = ttk.Treeview(self.order_frame, 
                                     columns=("ID", "Customer", "Product", "Quantity", "Status", "Date"), 
                                     show="headings")
        self.order_tree.heading("ID", text="Order ID")
        self.order_tree.heading("Customer", text="Customer ID")
        self.order_tree.heading("Product", text="Product ID")
        self.order_tree.heading("Quantity", text="Quantity")
        self.order_tree.heading("Status", text="Status")
        self.order_tree.heading("Date", text="Order Date")
        self.order_tree.pack(pady=10, fill="both", expand=True)
        
        self.load_orders()

    def place_order(self):
        customer_id = self.order_customer_id.get()
        product_id = self.order_product_id.get()
        quantity = self.order_quantity.get()
        status = self.order_status.get()
        
        if customer_id.isdigit() and product_id.isdigit() and quantity.isdigit() and status:
            if backend.place_order(customer_id, product_id, quantity, status):
                self.load_orders()
                self.load_inventory()
                self.check_restock_alerts()
                self.clear_order_fields()
            else:
                messagebox.showerror("Error", "Invalid product, customer, or insufficient stock")
        else:
            messagebox.showerror("Error", "Please enter valid details")

    def clear_order_fields(self):
        self.order_customer_id.delete(0, tk.END)
        self.order_product_id.delete(0, tk.END)
        self.order_quantity.delete(0, tk.END)
        self.order_status.delete(0, tk.END)

    def load_orders(self):
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        
        for row in backend.load_orders():
            self.order_tree.insert("", tk.END, values=row)

    # Supplier Tab
    def setup_supplier_tab(self):
        tk.Label(self.supplier_frame, text="Supplier Management",
                font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#bd34b6").pack(pady=10)
        
        entry_frame = ttk.Frame(self.supplier_frame, padding="10", style="Tab.TFrame")
        entry_frame.pack(fill="x")
        
        tk.Label(entry_frame, text="Supplier Name", bg="#e4eef1").pack()
        self.supplier_name = ttk.Entry(entry_frame)
        self.supplier_name.pack(pady=5, fill="x")
        
        tk.Label(entry_frame, text="Contact Details", bg="#f3fdff").pack()
        self.supplier_contact = ttk.Entry(entry_frame)
        self.supplier_contact.pack(pady=5, fill="x")
        
        tk.Label(entry_frame, text="Restocking Order Details", bg="#eff1f2").pack()
        self.supplier_restock = ttk.Entry(entry_frame)
        self.supplier_restock.pack(pady=5, fill="x")
        
        ttk.Button(entry_frame, text="Add Supplier", command=self.add_supplier,
                  style="Accent.TButton").pack(pady=5)
        
        # Transaction Fields
        tk.Label(entry_frame, text="Supplier ID", bg="#e1eff3").pack()
        self.transaction_supplier_id = ttk.Entry(entry_frame)
        self.transaction_supplier_id.pack(pady=5, fill="x")
        
        tk.Label(entry_frame, text="Transaction Amount", bg="#e9f1f3").pack()
        self.transaction_amount = ttk.Entry(entry_frame)
        self.transaction_amount.pack(pady=5, fill="x")
        
        tk.Label(entry_frame, text="Description", bg="#e9f2f5").pack()
        self.transaction_desc = ttk.Entry(entry_frame)
        self.transaction_desc.pack(pady=5, fill="x")
        
        ttk.Button(entry_frame, text="Add Transaction", command=self.add_transaction,
                  style="Accent.TButton").pack(pady=5)
        
        self.supplier_tree = ttk.Treeview(self.supplier_frame, 
                                        columns=("ID", "Name", "Contact", "Restock"), 
                                        show="headings")
        self.supplier_tree.heading("ID", text="Supplier ID")
        self.supplier_tree.heading("Name", text="Name")
        self.supplier_tree.heading("Contact", text="Contact")
        self.supplier_tree.heading("Restock", text="Restock Details")
        self.supplier_tree.pack(pady=10, fill="both", expand=True)
        
        self.load_suppliers()

    def add_supplier(self):
        name = self.supplier_name.get()
        contact = self.supplier_contact.get()
        restock = self.supplier_restock.get()
        
        if name and contact:
            backend.add_supplier(name, contact, restock)
            self.load_suppliers()
            self.clear_supplier_fields()
        else:
            messagebox.showerror("Error", "Please enter valid details")

    def add_transaction(self):
        supplier_id = self.transaction_supplier_id.get()
        amount = self.transaction_amount.get()
        desc = self.transaction_desc.get()
        
        if supplier_id.isdigit() and amount.replace('.', '', 1).isdigit():
            backend.add_transaction(supplier_id, amount, desc)
            self.clear_transaction_fields()
        else:
            messagebox.showerror("Error", "Please enter valid details")

    def clear_supplier_fields(self):
        self.supplier_name.delete(0, tk.END)
        self.supplier_contact.delete(0, tk.END)
        self.supplier_restock.delete(0, tk.END)

    def clear_transaction_fields(self):
        self.transaction_supplier_id.delete(0, tk.END)
        self.transaction_amount.delete(0, tk.END)
        self.transaction_desc.delete(0, tk.END)

    def load_suppliers(self):
        for item in self.supplier_tree.get_children():
            self.supplier_tree.delete(item)
        
        for row in backend.load_suppliers():
            self.supplier_tree.insert("", tk.END, values=row)

    # Customer Tab
    def setup_customer_tab(self):
        tk.Label(self.customer_frame, text="Customer Management",
                font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#b850ef").pack(pady=10)
        
        entry_frame = ttk.Frame(self.customer_frame, padding="10", style="Tab.TFrame")
        entry_frame.pack(fill="x")
        
        tk.Label(entry_frame, text="Customer Name", bg="#e3eef0").pack()
        self.customer_name = ttk.Entry(entry_frame)
        self.customer_name.pack(pady=5, fill="x")
        
        tk.Label(entry_frame, text="Contact Details", bg="#e8f0f3").pack()
        self.customer_contact = ttk.Entry(entry_frame)
        self.customer_contact.pack(pady=5, fill="x")
        
        ttk.Button(entry_frame, text="Add Customer", command=self.add_customer,
                  style="Accent.TButton").pack(pady=5)
        
        self.customer_tree = ttk.Treeview(self.customer_frame, 
                                        columns=("ID", "Name", "Contact"), 
                                        show="headings")
        self.customer_tree.heading("ID", text="Customer ID")
        self.customer_tree.heading("Name", text="Name")
        self.customer_tree.heading("Contact", text="Contact")
        self.customer_tree.pack(pady=10, fill="both", expand=True)
        
        self.load_customers()

    def add_customer(self):
        name = self.customer_name.get()
        contact = self.customer_contact.get()
        
        if name and contact:
            backend.add_customer(name, contact)
            self.load_customers()
            self.clear_customer_fields()
        else:
            messagebox.showerror("Error", "Please enter valid details")

    def clear_customer_fields(self):
        self.customer_name.delete(0, tk.END)
        self.customer_contact.delete(0, tk.END)

    def load_customers(self):
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        for row in backend.load_customers():
            self.customer_tree.insert("", tk.END, values=row)

    # Report Tab
    def setup_report_tab(self):
        tk.Label(self.report_frame, text="Reports",
                font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#b455ef").pack(pady=10)
        ttk.Button(self.report_frame, text="Generate Sales Report", 
                  command=self.generate_sales_report, style="Accent.TButton").pack(pady=5)
        
        self.report_text = tk.Text(self.report_frame, height=20, width=60, 
                                 bg="white", font=("Arial", 10))
        self.report_text.pack(pady=10)

    def generate_sales_report(self):
        orders, df = backend.generate_sales_report()
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, "Sales Report\n\n")
        for order in orders:
            self.report_text.insert(tk.END, f"Order ID: {order[0]}\n")
            self.report_text.insert(tk.END, f"Customer: {order[1]}\n")
            self.report_text.insert(tk.END, f"Product: {order[2]}\n")
            self.report_text.insert(tk.END, f"Quantity: {order[3]}\n")
            self.report_text.insert(tk.END, f"Status: {order[4]}\n")
            self.report_text.insert(tk.END, f"Date: {order[5]}\n\n")
        
        # Generate Plot
        plt.figure(figsize=(8, 6))
        plt.bar(df['name'], df['total'], color="#7eb2f7")
        plt.xlabel('Product')
        plt.ylabel('Total Quantity Sold')
        plt.title('Sales by Product')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('sales_report.png')
        plt.close()

# Run Application
def start_main_app():
    main_root = tk.Tk()
    app = InventoryApp(main_root)
    main_root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()
    login_app = LoginWindow(login_root, start_main_app)
    login_root.mainloop()