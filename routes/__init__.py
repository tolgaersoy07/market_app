from flask import Blueprint
from .login import login_bp
from .register import register_bp
from .logout import logout_bp
from .forgotten_password_validate import forgotten_password_validate_bp
from .dashboard import dashboard_bp
from .user_info import user_info_bp
from .access_token_validate import access_token_validate_bp
from .orders import orders_bp 
from .cart import cart_bp
from .top_up_balance import top_up_balance_bp
from .scan_barcode import scan_barcode_bp

#Aşağıdakinler /admin için.
from .admin.admin import admin_bp 
from .admin.sales import sales_bp
from .admin.add_products import add_products_bp
from .admin.product_list import product_list_bp
from .admin.customer import customer_bp
from .admin.withdraw_money import withdraw_money_bp
from .admin.product_operation import product_operation_bp

def register_blueprints(app):
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(logout_bp)  
    app.register_blueprint(forgotten_password_validate_bp)
    app.register_blueprint(dashboard_bp)
    
    app.register_blueprint(user_info_bp)
    app.register_blueprint(access_token_validate_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(top_up_balance_bp)
    app.register_blueprint(scan_barcode_bp)

    #Aşağıdakinler /admin için.
    app.register_blueprint(admin_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(add_products_bp)
    app.register_blueprint(product_list_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(withdraw_money_bp)
    app.register_blueprint(product_operation_bp)