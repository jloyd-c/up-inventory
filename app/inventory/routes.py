from flask import Blueprint, render_template

inventory_bp = Blueprint('inventory', __name__,
                         template_folder='templates',
                         url_prefix='/inventory')

@inventory_bp.route('/')
def inventory_home():
    return render_template('inventory.html')
