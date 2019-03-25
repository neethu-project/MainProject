from flask import *
import MySQLdb
import os
from werkzeug.utils import secure_filename
con=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306,db='arbuilding')
cmd=con.cursor()
root=Flask(__name__)
path="C:\\Users\\NEETHU\\PycharmProjects\\arbuilding\\arb\\static\\image"
root.secret_key="arbuilding"

@root.route('/')
def main_page():
    return render_template('main_page.html')

@root.route('/ext_signup')
def ext_signup():
    return render_template('ex_reg_ext.html')

@root.route('/arch_signup')
def arch_signup():
    return render_template('ar_reg_arch.html')

@root.route('/login')
def login():
    return render_template('login1.html')
@root.route('/log',methods=['get','post'])
def log():
    usnm=request.form['textfield']
    pswrd=request.form['textfield2']
    cmd.execute("select * from login where user_name='"+usnm+"' and password='"+pswrd+"'")
    s=cmd.fetchone()
    print(s)
    if s is None:
        return '''<script>alert('Invalid Username or Password');window.location='/'</script>'''
    elif(s[3]=='Admin'):
        return render_template('a_home_page.html')
    elif(s[3]=='Architect'):
        return render_template('ar_home_page.html')
    else:
        return render_template('ex_home_page.html')

@root.route('/a_home_page')
def a_home_page():
    return render_template('a_home_page.html')


@root.route('/ex_home_page')
def ex_home_page():
    return render_template('ex_home_page.html')

@root.route('/log_out')
def log_out():
    return render_template('login.html')


@root.route('/reg_arch')
def reg_arch():
    return render_template('ar_reg_arch.html')
@root.route('/arch_reg',methods=['get','post'])
def arch_reg():
    fnm=request.form['textfield']
    lnm=request.form['textfield12']
    dob=request.form['textfield22']
    age=request.form['textfield2']
    gender=request.form['radiobutton']
    lno=request.form['textfield3']
    quali1=request.form['textfield4']
    quali2=request.form['textfield5']
    quali3=request.form['textfield6']
    exp=request.form['textfield7']
    comp=request.form['textfield8']
    email=request.form['textfield9']
    print(email)
    pnno=request.form['textfield10']
    print(pnno)
    land=request.form['textfield11']
    photo=request.files['file']
    img=secure_filename(photo.filename)
    photo.save(os.path.join(path,img))
    cmd.execute("insert into login values(null,'"+email+"','"+dob+"','pending')")
    id=con.insert_id()
    cmd.execute("insert into reg_arch values('"+str(id)+"','"+fnm+"','"+lnm+"','"+dob+"','"+gender+"','"+lno+"','"+quali1+"','"+quali2+"','"+quali3+"','"+exp+"','"+comp+"','"+email+"','"+pnno+"','"+land+"','"+img+"','"+age+"')")
    con.commit()
    return '''<script>alert("Insert Successfully");window.location="/"</script>'''


@root.route('/reg_ext')
def reg_ext():
    return render_template('ex_reg_ext.html')
@root.route('/ext_reg',methods=['get','post'])
def ext_reg():
    fnm=request.form['textfield']
    lnm=request.form['textfield11']
    dob=request.form['textfield2']
    age=request.form['textfield3']
    gender=request.form['radiobutton']
    quali1=request.form['textfield4']
    quali2=request.form['textfield5']
    exp=request.form['textfield6']
    comp=request.form['textfield7']
    email=request.form['textfield8']
    pnno=request.form['textfield9']
    land=request.form['textfield10']
    photo=request.files['file']
    img=secure_filename(photo.filename)
    photo.save(os.path.join(path,img))
    cmd.execute("insert into login values(null,'"+email+"','"+dob+"','pending')")
    id=con.insert_id()
    cmd.execute("insert into reg_ext values('"+str(id)+"','"+fnm+"','"+lnm+"','"+dob+"','"+age+"','"+gender+"','"+quali1+"','"+quali2+"','"+exp+"','"+comp+"','"+email+"','"+pnno+"','"+land+"','"+img+"')")
    con.commit()
    return '''<script>alert("Insert Successfully");window.location="/"</script>'''


@root.route('/a_aprv_arch')
def a_aprv_arch():
    cmd.execute("SELECT `reg_arch`.* FROM `reg_arch` JOIN `login` ON `login`.lid=`reg_arch`.`arch_id` WHERE `login`.type='pending'")
    s = cmd.fetchall()
    print(s)
    return render_template('a_aprv_arch.html',val=s)
@root.route('/a_approved_arch')
def a_approved_arch():
    id=request.args.get('id')
    cmd.execute("UPDATE login SET type='Architect' WHERE lid='"+str(id)+"'")
    con.commit()
    return '''<script>alert('Approved');window.location="/a_aprv_arch"</script>'''


@root.route('/a_aprv_ext')
def a_aprv_ext():
    cmd.execute("SELECT `reg_ext`.* FROM `reg_ext` JOIN `login` ON `login`.lid=`reg_ext`.`ext_id` WHERE `login`.type='pending'")
    s = cmd.fetchall()
    print(s)
    return render_template('a_aprv_ext.html',val=s)
@root.route('/a_approved_ext')
def a_approved_ext():
    id = request.args.get('id')
    cmd.execute("UPDATE login SET type='Exterior' WHERE lid='"+str(id)+"'")
    con.commit()
    return '''<script>alert('Approved');window.location="/a_aprv_ext"</script>'''


@root.route('/a_view_arch')
def a_view_arch():
    cmd.execute("SELECT `reg_arch`.`arch_id`,f_name,photo FROM `reg_arch` JOIN `login`ON `login`.`lid`=`reg_arch`.`arch_id`WHERE `login`.type!='pending'")
    # cmd.execute("SELECT `reg_arch`.`arch_id`,f_name,photo FROM `reg_arch`")
    s=cmd.fetchall()
    return render_template('a_view_arch.html',val=s)
@root.route('/a_vmp_arch')
def a_vmp_arch():
    id = request.args.get('id')
    cmd.execute("SELECT * FROM `reg_arch` WHERE arch_id='"+str(id)+"'")
    s=cmd.fetchone()
    return render_template('a_vmp_arch.html',d=s)

@root.route('/a_view_ext')
def a_view_ext():
    cmd.execute("SELECT `reg_ext`.`ext_id`,f_name,photo FROM `reg_ext` JOIN `login`ON `login`.`lid`=`reg_ext`.`ext_id`WHERE `login`.type!='pending'")
    # cmd.execute("SELECT `reg_ext`.`ext_id`,f_name,photo FROM `reg_ext`")
    s = cmd.fetchall()
    return render_template('a_view_ext.html',val=s)
@root.route('/a_vmp_ext')
def a_vmp_ext():
    id = request.args.get('id')
    cmd.execute("SELECT * FROM `reg_ext` WHERE ext_id='" + str(id) + "'")
    s = cmd.fetchone()
    return render_template('a_vmp_ext.html',d=s)


@root.route('/a_vplan')
def a_vplan():
    cmd.execute("SELECT `plan`.`plan_id`,`plan`.`upload_img1`,`reg_arch`.`f_name`,`reg_arch`.`l_name`,`reg_arch`.`photo` FROM `plan` JOIN `reg_arch` ON `reg_arch`.`arch_id`=`plan`.`arch_id`")
    s=cmd.fetchall()
    return render_template('a_vplan.html',val=s)
@root.route('/a_view_plan_more')
def a_view_plan_more():
    id = request.args.get('id')
    cmd.execute("SELECT `plan`.`plan_id`,`plan`.`upload_img1`,`plan`.`description1`,`plan`.`upload_img2`,`plan`.`description2`,`plan`.`upload_img3`,`plan`.`description3`,`reg_arch`.`f_name`,`reg_arch`.`l_name`,`reg_arch`.`photo` FROM `plan` JOIN`reg_arch`ON`reg_arch`.`arch_id`=`plan`.`arch_id` WHERE plan_id='" + str(id) + "'")
    s = cmd.fetchone()
    return render_template('a_view_plan_more.html',d=s)


@root.route('/a_vdesign')
def a_vdesign():
    cmd.execute("SELECT `design`.`des_id`,`design`.`upload_img1`,`reg_ext`.`f_name`,`reg_ext`.`l_name`,`reg_ext`.`photo` FROM `design` JOIN `reg_ext` ON `reg_ext`.`ext_id`=`design`.`ext_id`")
    s=cmd.fetchall()
    return  render_template('a_vdesign.html',val=s)
@root.route('/a_view_design_more')
def a_vmdesign():
    id = request.args.get('id')
    cmd.execute("SELECT * FROM `plan` WHERE plan_id='" + str(id) + "'")
    s = cmd.fetchone()
    return render_template('a_view_design_more.html',d=s)


@root.route('/a_view_comptitle')
def a_view_comptitle():
    cmd.execute("SELECT `complaints`.`comp_id`,`complaints`.`cust_id`,`complaints`.`date`,`complaints`.`subject`,`reg_cust`.`f_name`,`reg_cust`.`l_name` FROM `complaints`JOIN `reg_cust` ON `reg_cust`.`cust_id`=`complaints`.`cust_id`")
    s=cmd.fetchall()
    return render_template('a_view_comptitle.html',val=s)
@root.route('/a_rplycomp')
def a_rplycomp():
    id = request.args.get('id')
    cmd.execute("SELECT `complaints`.*,`reg_cust`.`f_name`,`reg_cust`.`l_name`,`reg_arch`.`f_name`,`reg_arch`.`l_name` FROM `complaints` JOIN `reg_cust`ON `reg_cust`.`cust_id`=`complaints`.`cust_id`JOIN `reg_arch` ON `reg_arch`.`arch_id`=`complaints`.`reg_id` UNION SELECT `complaints`.*,`reg_cust`.`f_name`,`reg_cust`.`l_name`,`reg_ext`.`f_name`,`reg_ext`.`l_name` FROM `complaints` JOIN `reg_cust`ON `reg_cust`.`cust_id`=`complaints`.`cust_id`JOIN `reg_ext` ON `reg_ext`.`ext_id`=`complaints`.`reg_id` WHERE comp_id='" + str(id) + "'")
    s = cmd.fetchone()
    return render_template('a_rplycomp.html',d=s)

@root.route('/a_view_rating')
def a_view_rating():
    cmd.execute("SELECT `rating`.*,`reg_arch`.`f_name`,`reg_arch`.`l_name`,`reg_arch`.`photo`FROM `rating`JOIN`reg_arch`ON`reg_arch`.`arch_id`=`rating`.`acc_id`UNION SELECT `rating`.*,`reg_ext`.`f_name`,`reg_ext`.`l_name`,`reg_ext`.`photo` FROM `rating`JOIN `reg_ext` ON `reg_ext`.`ext_id`=`rating`.`acc_id`")
    s=cmd.fetchall()
    return render_template('a_view_rating.html',val=s,d=s)




@root.route('/ar_home_page')
def ar_home_page():
    return render_template('ar_home_page.html')

















@root.route('/changepass')
def changepass():
    return render_template('login2.html')







if(__name__=='__main__'):
    root.run(debug=True)



