from flask import Flask,render_template,url_for,request,flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,EmailField,IntegerField
from wtforms.validators import DataRequired,email_validator
import boto3

ddb = boto3.resource('dynamodb',region_name='us-east-1')
Customer_table = ddb.Table('Customers')
Product_table = ddb.Table('products')
Order_table = ddb.Table('orders')
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'MY secret key' # to use forms we need secret key
# Form class
class editform(FlaskForm):
    #CustomerID = StringField('Customer_name',validators=[DataRequired()])
    CompanyName = StringField('Company_name',validators=[DataRequired()])
    ContactName = StringField('Contact_name',validators=[DataRequired()])
    ContactTitle = StringField('Contact_title',validators=[DataRequired()])
    Address = StringField('Address',validators=[DataRequired()])
    City = StringField('City',validators=[DataRequired()])
    Region = StringField('Region',validators=[DataRequired()])
    PostalCode = StringField('Postal_code',validators=[DataRequired()])
    Country = StringField('Country',validators=[DataRequired()])
    Phone = StringField('Phone',validators=[DataRequired()])
    Fax = StringField('Fax',validators=[DataRequired()])
    Add = SubmitField('Add Customer')

# Create a edit route decorator
@app.route('/editcustomer/<customer_id>',methods=['GET','POST'])
def edit(customer_id):
    form = editform()
    name_to_update = Customer_table.get_item(Key={'CustomerID':customer_id})['Item']
    if request.method == 'POST':
        update = name_to_update
        for i in ["CompanyName","ContactName","ContactTitle","Address","City","Region", "PostalCode","Country","Phone",'Fax']:
            update[i] = request.form[i]
        d = request.form.to_dict()
        #d.pop('CustomerID')
        attribute_updates = {key:{'Value':value,'Action':'PUT'} for key,value in d.items()}
        try:
            Customer_table.update_item(Key = {'CustomerID':customer_id},AttributeUpdates = attribute_updates)
            flash('Customer updated')
            return render_template('edit.html',name_to_update=update,form=form,customer_id=customer_id)
        except:
            flash('ERROR Customer not updated')
            return render_template('edit.html',name_to_update=name_to_update,form=form,customer_id=customer_id)
    else:
        
        return render_template('edit.html',name_to_update=name_to_update,form=form,customer_id=customer_id)


# Product form class
class product_form(FlaskForm):
    #ProductID = IntegerField('ProductID',validators=[DataRequired()])
    ProductName = StringField('ProductName',validators=[DataRequired()])
    SupplierID = IntegerField('SupplierID',validators=[DataRequired()])
    CategoryID = IntegerField('CategoryID',validators=[DataRequired()])
    QuantityPerUnit = StringField('QuantityPerUnit',validators=[DataRequired()])
    UnitPrice = IntegerField('UnitPrice',validators=[DataRequired()])
    UnitsInStock = IntegerField('UnitsInStock',validators=[DataRequired()])
    UnitsOnOrder = IntegerField('UnitsOnOrder',validators=[DataRequired()])
    ReorderLevel = IntegerField('ReorderLevel',validators=[DataRequired()])
    Discontinued = IntegerField('Discontinued',validators=[DataRequired()])
    Add = SubmitField('update Product')

# Create a edit route decorator
@app.route('/editproduct/<product_id>',methods=['GET','POST'])
def edit_product(product_id):
    form = product_form()
    product_to_update = Product_table.get_item(Key={'ProductID':product_id})['Item']
    if request.method == 'POST':
        for i in ['ProductName','SupplierID','CategoryID','QuantityPerUnit','UnitPrice','UnitsInStock','UnitsOnOrder','ReorderLevel','Discontinued']:
           product_to_update[i] = request.form[i] 
        attribute_updates = {key:{'Value':value,'Action':'PUT'} for key,value in request.form.items()}
        try:
            flash('Product updated')
            Product_table.update_item(Key = {'ProductID':product_id},AttributeUpdates = attribute_updates)
            return render_template('product_edit.html',product_to_update=product_to_update,form=form,product_id = product_id)
        except:
            flash('ERROR Product not updated')
            return render_template('product_edit.html',product_to_update=product_to_update,form=form,product_id = product_id)
    else:
        return render_template('product_edit.html',product_to_update=product_to_update,form=form,product_id = product_id)


# order table form
class orderform(FlaskForm):
    #OrderID = StringField('OrderID',validators=[DataRequired()])
    CustomerID = StringField('CustomerID',validators=[DataRequired()])
    EmployeeID = IntegerField('Discontinued',validators=[DataRequired()])
    OrderDate = StringField('OrderDate',validators=[DataRequired()])
    RequiredDate = StringField('RequiredDate',validators=[DataRequired()])
    ShippedDate = StringField('ShippedDate',validators=[DataRequired()])
    ShipVia = IntegerField('Discontinued',validators=[DataRequired()])
    Freight = IntegerField('Discontinued',validators=[DataRequired()])
    ShipName = StringField('ShipName',validators=[DataRequired()])
    ShipAddress = StringField('ShipAddress',validators=[DataRequired()])
    ShipCity = StringField('ShipCity',validators=[DataRequired()])
    ShipRegion = StringField('ShipRegion',validators=[DataRequired()])
    ShipPostalCode = StringField('ShipPostalCode',validators=[DataRequired()])
    ShipCountry = StringField('ShipCountry',validators=[DataRequired()])
    Add = SubmitField('update order')

@app.route('/editorder/<order_id>',methods = ['GET','POST'])
def edit_order(order_id):
    form = orderform()
    order_to_update = Order_table.get_item(Key={'OrderID':order_id})['Item']
    if request.method == 'POST':
        for i in ['CustomerID','EmployeeID','OrderDate','RequiredDate','ShippedDate','ShipVia','Freight','ShipName','ShipAddress','ShipCity','ShipRegion','ShipPostalCode','ShipCountry']:
            order_to_update[i] = request.form[i]
        attribute_updates = {key:{'Value':value,'Action':'PUT'} for key,value in request.form.items()}
        try:
            
            flash('Order updated')
            Order_table.update_item(Key = {'OrderID':order_id},AttributeUpdates = attribute_updates)
            return render_template('order_edit.html',order_to_update=order_to_update,form=form,order_id = order_id)
        except:
            flash('ERROR order not updated')
            return render_template('order_edit.html',order_to_update=order_to_update,form=form,order_id = order_id)
    else:
        return render_template('order_edit.html',order_to_update=order_to_update,form=form,order_id = order_id)




@app.route('/')
def homepage():
    return render_template('homepage.html',title='Homepage')

@app.route('/customertable',methods=['GET','POST'])
def customer_table():
    data = Customer_table.scan()['Items']
    return render_template('customer_table.html',title='Customer Table',table_name = "Customer Table",data = data)

@app.route('/producttable')
def product_table():
    data = Product_table.scan()['Items']
    return render_template("product_table.html",title = "Product table",table_name = "Product Table",data = data)

@app.route('/ordertable')
def order_table():
    data = Order_table.scan()['Items']
    return render_template("order_table.html",title = "Order table",table_name = "Order Table",data = data)

# search fucntion
class searchform(FlaskForm):
    searched = StringField('searched',validators=[DataRequired()])
    submit = SubmitField('submit')

@app.route('/search',methods = ['POST'])
def search():
    form = searchform()
    customer_id = None
    if request.method == 'POST':
        customer_id = form.searched.data
        data = Order_table.query(
                    TableName='orders',
                    IndexName='CustomerID-index',
                    Select='ALL_ATTRIBUTES',
                    KeyConditions={'CustomerID': { 'AttributeValueList': [customer_id] ,'ComparisonOperator': 'EQ'} }
                    )['Items']
        return render_template('search.html',form=form,customer_id = customer_id,data=data)


class cust_delete_form(FlaskForm):
    id = StringField('CustomerID',validators=[DataRequired()])
    delete  = SubmitField('Delete')

@app.route('/deletecustomer',methods = ['POST','GET'])
def delete_customer():
    form = cust_delete_form()
    to_delete = None
    if request.method == 'POST':
        to_delete = request.form['id']
        try:
            check = Customer_table.get_item(Key={'CustomerID':to_delete})['Item']
            Customer_table.delete_item(Key = {'CustomerID':to_delete})
            form.id.data = ''
            flash(f'Customer {to_delete} has been Deleted')
            return render_template('delete.html',form=form,table = 'customer_table',name = 'Customer',route = '/deletecustomer')
        except KeyError:
            flash(f'The Customer {to_delete} does not exist in the customer table')
            form.id.data = ''
            return render_template('delete.html',form=form,table = 'customer_table',name = 'Customer',route = '/deletecustomer')
    else:
        form.id.data = ''
        return render_template('delete.html',form=form,table = 'customer_table',name = 'Customer',route = '/deletecustomer')

class prod_delete_form(FlaskForm):
    id = StringField('ProductID',validators=[DataRequired()])
    delete  = SubmitField('Delete')

@app.route('/deleteproduct',methods = ['POST','GET'])
def delete_product():
    form = prod_delete_form()
    to_delete = None
    if request.method == 'POST':
        to_delete = request.form['id']
        try:
            check = Product_table.get_item(Key={'ProductID':to_delete})['Item']
            Product_table.delete_item(Key = {'ProductID':to_delete})
            form.id.data = ''
            flash(f'Product {to_delete} has been Deleted')
            return render_template('delete.html',form=form,table = 'product_table',name = 'Product',route = '/deleteproduct')
        except KeyError:
            flash(f'The Product {to_delete} does not exist in the product table')
            form.id.data = ''
            return render_template('delete.html',form=form,table = 'product_table',name = 'Product',route = '/deleteproduct')
    else:
        form.id.data = ''
        return render_template('delete.html',form=form,table = 'product_table',name = 'Product',route = '/deleteproduct')


class order_delete_form(FlaskForm):
    id = StringField('OrderID',validators=[DataRequired()])
    delete  = SubmitField('Delete')

@app.route('/deleteorder',methods = ['POST','GET'])
def delete_order():
    form = order_delete_form()
    to_delete = None
    if request.method == 'POST':
        to_delete = request.form['id']
        try:
            check = Order_table.get_item(Key={'OrderID':to_delete})['Item']
            Order_table.delete_item(Key = {'OrderID':to_delete})
            form.id.data = ''
            flash(f'Order {to_delete} has been Deleted')
            return render_template('delete.html',form=form,table = 'order_table',name = 'Order',route = '/deleteorder')
        except KeyError:
            flash(f'The Order {to_delete} does not exist in Order table')
            form.id.data = ''
            return render_template('delete.html',form=form,table = 'order_table',name = 'Order',route = '/deleteorder')
    else:
        form.id.data = ''
        return render_template('delete.html',form=form,table = 'order_table',name = 'Order',route = '/deleteorder')



if __name__ =='__main__':
    app.run(debug=True)