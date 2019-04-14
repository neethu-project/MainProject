from flask import *
import MySQLdb
import os
from werkzeug.utils import secure_filename
con=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306,db='arbuilding')
cmd=con.cursor()
root=Flask(__name__)
path="C:\\Users\\NEETHU\\PycharmProjects\\arbuilding\\arb\\static\\image"
plan_path="C:\\Users\\NEETHU\\PycharmProjects\\arbuilding\\arb\\static\\uploadplan"
des_path="C:\\Users\\NEETHU\\PycharmProjects\\arbuilding\\arb\\static\\uploaddesign"
root.secret_key="arbuilding"



@root.route('/')
def main_page():
    return render_template('main_page.html')

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


@root.route('/ext_signup')
def ext_signup():
    return render_template('ex_reg_ext.html')

@root.route('/login')
def login():
    return render_template('login1.html')
@root.route('/login_action',methods=['get','post'])
def login_action():
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
        id=s[0]
        session['arid']=id
        return render_template('ar_home_page.html')
    else:
        session['exid']=s[0]
        return render_template('ex_home_page.html')

#ADMIN
@root.route('/a_home_page')
def a_home_page():
    return render_template('a_home_page.html')


@root.route('/log_out')
def log_out():
    return render_template('login.html')



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




#ADMIN


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
@root.route('/a_reject_arch')
def a_reject_arch():
    id=request.args.get('id')
    cmd.execute("UPDATE login SET type='Reject' WHERE lid='"+str(id)+"'")
    con.commit()
    return '''<script>alert('Rejected');window.location="/a_aprv_arch"</script>'''


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
@root.route('/a_reject_ext')
def a_reject_ext():
    id = request.args.get('id')
    cmd.execute("UPDATE login SET type='Reject' WHERE lid='"+str(id)+"'")
    con.commit()
    return '''<script>alert('Rejected');window.location="/a_aprv_ext"</script>'''


@root.route('/a_view_arch')
def a_view_arch():
    cmd.execute("SELECT `reg_arch`.`arch_id`,f_name,photo FROM `reg_arch` JOIN `login`ON `login`.`lid`=`reg_arch`.`arch_id`WHERE `login`.type!='pending'")
    s=cmd.fetchall()
    return render_template('a_view_arch.html',val=s)
@root.route('/a_view_arch_more')
def a_view_arch_more():
    id = request.args.get('id')
    cmd.execute("SELECT * FROM `reg_arch` WHERE arch_id='"+str(id)+"'")
    s=cmd.fetchone()
    return render_template('a_view_arch_more.html',d=s)


@root.route('/a_view_ext')
def a_view_ext():
    cmd.execute("SELECT `reg_ext`.`ext_id`,f_name,photo FROM `reg_ext` JOIN `login`ON `login`.`lid`=`reg_ext`.`ext_id`WHERE `login`.type!='pending'")
    s = cmd.fetchall()
    return render_template('a_view_ext.html',val=s)
@root.route('/a_view_ext_more')
def a_view_ext_more():
    id = request.args.get('id')
    cmd.execute("SELECT * FROM `reg_ext` WHERE ext_id='" + str(id) + "'")
    s = cmd.fetchone()
    return render_template('a_view_ext_more.html',d=s)


@root.route('/a_view_plan')
def a_view_plan():
    cmd.execute("SELECT `plan`.`plan_id`,`plan_img`.`upload_img1`,`reg_arch`.`f_name`,`reg_arch`.`l_name`,`reg_arch`.`photo` FROM`reg_arch`JOIN`plan`ON `plan`.`arch_id`=`reg_arch`.`arch_id` JOIN`plan_img`ON`plan_img`.`plan_id`=`plan`.`plan_id` WHERE STATUS='Approved' GROUP BY plan_id")
    # cmd.execute("SELECT `plan`.`plan_id`,`plan_img`.`upload_img1`,`reg_arch`.`f_name`,`reg_arch`.`l_name`,`reg_arch`.`photo` FROM`reg_arch`JOIN`plan`ON `plan`.`arch_id`=`reg_arch`.`arch_id` JOIN`plan_img`ON`plan_img`.`plan_id`=`plan`.`plan_id` WHERE status='Approved'")
    s=cmd.fetchall()
    return render_template('a_view_plan.html',val=s)
@root.route('/a_view_plan_more')
def a_view_plan_more():
    id = request.args.get('id')
    session['id']=id
    cmd.execute("SELECT `plan`.*,`plan_img`.`upload_img1`,`reg_arch`.`f_name`,`reg_arch`.`l_name`,`reg_arch`.`photo` FROM`reg_arch`JOIN`plan`ON `plan`.`arch_id`=`reg_arch`.`arch_id` JOIN`plan_img`ON`plan_img`.`plan_id`=`plan`.`plan_id` WHERE `plan`. plan_id='" + str(id) + "'")
    s = cmd.fetchone()
    cmd.execute("SELECT `upload_img1` FROM `plan_img` WHERE `plan_id`='"+str(id)+"'")
    s1=cmd.fetchall()
    return render_template('a_view_plan_more.html',d=s,v=s1)
@root.route('/a_reject_plan',methods=['get','post'])
def a_reject_plan():
    id=session['id']
    print(id)
    cmd.execute("UPDATE plan SET status='Reject' WHERE plan_id='"+str(id)+"'")
    con.commit()
    return '''<script>alert('Rejected');window.location="/a_view_plan"</script>'''



@root.route('/a_view_design')
def a_view_design():
    cmd.execute("SELECT `design`.`des_id`,`design_img`.`upload_img`,`reg_ext`.`f_name`,`reg_ext`.`l_name`,`reg_ext`.`photo` FROM `reg_ext`JOIN `design`ON `design`.`ext_id`=`reg_ext`.`ext_id` JOIN `design_img`ON `design_img`.`des_id`=`design`.`des_id` WHERE design.status='Approved' GROUP BY des_id")
    s=cmd.fetchall()
    return  render_template('a_view_design.html',val=s)
@root.route('/a_view_design_more')
def a_view_design_more():
    id = request.args.get('id')
    session['id']=id
    cmd.execute("SELECT `design`.*,`design_img`.`upload_img`,`reg_ext`.`f_name`,`reg_ext`.`l_name`,`reg_ext`.`photo` FROM `reg_ext`JOIN `design`ON `design`.`ext_id`=`reg_ext`.`ext_id` JOIN `design_img` ON `design_img`.`des_id`=`design`.`des_id` WHERE design.des_id='"+ str(id)+"'")
    s = cmd.fetchone()
    cmd.execute("SELECT `upload_img` FROM `design_img` WHERE `des_id`='" + str(id) + "'")
    s1 = cmd.fetchall()
    return render_template('a_view_design_more.html', d=s, v=s1)
@root.route('/a_reject_design',methods=['get','post'])
def a_reject_design():
    id=session['id']
    cmd.execute("UPDATE design SET status='Reject' WHERE des_id='"+str(id)+"'")
    con.commit()
    return '''<script>alert('Rejected');window.location="/a_view_design"</script>'''



@root.route('/a_view_comptitle')
def a_view_comptitle():
    cmd.execute("SELECT `complaints`.`comp_id`,`complaints`.`cust_id`,`complaints`.`date`,`complaints`.`subject`,`reg_cust`.`f_name`,`reg_cust`.`l_name` FROM `complaints`JOIN `reg_cust` ON `reg_cust`.`cust_id`=`complaints`.`cust_id` where `complaints`.`reply`='pending'")
    s=cmd.fetchall()
    return render_template('a_view_comptitle.html',val=s)
@root.route('/a_view_comp_rply')
def a_view_comp_rply():
    id = request.args.get('id')
    session['idd']=id
    print(id)
    cmd.execute("SELECT `complaints`.*,`reg_cust`.`f_name`,`reg_cust`.`l_name`,`reg_arch`.`f_name`,`reg_arch`.`l_name` FROM `complaints` JOIN `reg_cust`ON `reg_cust`.`cust_id`=`complaints`.`cust_id`JOIN `reg_arch` ON `reg_arch`.`arch_id`=`complaints`.`reg_id` where complaints.comp_id='"+str(id)+"'  UNION SELECT `complaints`.*,`reg_cust`.`f_name`,`reg_cust`.`l_name`,`reg_ext`.`f_name`,`reg_ext`.`l_name` FROM `complaints` JOIN `reg_cust`ON `reg_cust`.`cust_id`=`complaints`.`cust_id`JOIN `reg_ext` ON `reg_ext`.`ext_id`=`complaints`.`reg_id` WHERE complaints.comp_id='" + str(id) + "'")
    s = cmd.fetchone()
    print(s)
    return render_template('a_view_comp_rply.html',d=s)
@root.route('/a_sendreplay',methods=['get','post'])
def a_sendreplay():
    id=session['idd']
    rply=request.form['textarea']
    cmd.execute("update complaints set reply='"+rply+"' where comp_id='"+str(id)+"'")
    con.commit()
    return '''<script>alert("Send Reply Message");window.location="/a_view_comptitle"</script>'''


@root.route('/a_view_rating')
def a_view_rating():
    cmd.execute("SELECT `rating`.*,`reg_arch`.`f_name`,`reg_arch`.`l_name`,`reg_arch`.`photo`FROM `rating`JOIN`reg_arch`ON`reg_arch`.`arch_id`=`rating`.`acc_id`UNION SELECT `rating`.*,`reg_ext`.`f_name`,`reg_ext`.`l_name`,`reg_ext`.`photo` FROM `rating`JOIN `reg_ext` ON `reg_ext`.`ext_id`=`rating`.`acc_id`")
    s=cmd.fetchall()
    return render_template('a_view_rating.html',val=s,d=s)


#ARCHITECT

@root.route('/ar_home_page')
def ar_home_page():
    return render_template('ar_home_page.html')


# --------------------------------------UPLOAD PLANS-----------------------------------------------------------------------------------


@root.route('/ar_upload_plan')
def ar_upload_plan():
    return render_template('ar_upload_plan.html')


@root.route('/ar_upload_plan_action',methods=['get','post'])
def ar_upload_plan_action():
    pa=request.form['textfield']
    sf=request.form['textfield2']
    rm=request.form['textfield3']
    brm=request.form['textfield4']
    st=request.form['textfield5']
    cp=request.form['textfield6']
    fa=request.form['textfield7']
    od=request.form['textarea']
    tle=request.form['textfield8']
    arid=session['arid']
    cmd.execute("insert into plan values(null,'"+str(arid)+"','"+pa+"','"+sf+"','"+rm+"','"+brm+"','"+st+"','"+cp+"','"+fa+"','"+od+"','"+tle+"','Approved')")
    id = con.insert_id()
    session['plan_id'] = id
    print(id)
    con.commit()
    return '''<script>alert("Do you want to upload images");window.location="/ar_upload_plan_img"</script>'''


@root.route('/ar_upload_plan_img',methods=['get','post'])
def ar_upload_plan_img():
    return render_template('ar_upload_plan_img.html')


@root.route('/ar_upload_plan_img_action',methods=['get','post'])
def ar_upload_plan_img_action():
    bt1=request.form['Submit']
    if bt1=='Next':
        photo = request.files['file']
        img = secure_filename(photo.filename)
        photo.save(os.path.join(plan_path, img))
        plan_id = session['plan_id']
        print(plan_id)
        cmd.execute("insert into plan_img value(null,'" + str(plan_id) + "','" + img + "')")
        con.commit()
        return '''<script>alert("Do you want to upload the next image");window.location="/ar_upload_plan_img"</script>'''
    else:
        return '''<script>alert("Finished");window.location="/ar_home_page"</script>'''


# --------------------------------------VIEW UPLOAD PLANS-----------------------------------------------------------------------------------


@root.route('/ar_view_upload_plan')
def ar_view_upload_plan():
    cmd.execute("SELECT `plan`.`plan_id`,`plan`.`plan_title`,`plan_img`.`upload_img1` FROM`plan` JOIN`plan_img`ON`plan_img`.`plan_id`=`plan`.`plan_id` WHERE `plan`.`status`='Approved' AND `plan`.`arch_id`='"+str(session['arid'])+"' GROUP BY plan_id")
    # cmd.execute("SELECT plan_id,upload_img1 FROM plan WHERE arch_id='"+str(session['arid'])+"'")
    s = cmd.fetchall()
    return render_template('ar_view_upload_plan.html',val=s)


@root.route('/ar_view_upload_plan_more')
def ar_view_upload_plan_more():
    plan_id = request.args.get('id')
    session['id'] = plan_id
    cmd.execute("SELECT `plan`.*,`plan_img`.`upload_img1` FROM plan JOIN`plan_img`ON`plan_img`.`plan_id`=`plan`.`plan_id` WHERE `plan`. plan_id='" + str(plan_id) + "'")
    s = cmd.fetchone()
    cmd.execute("SELECT `upload_img1` FROM `plan_img` WHERE `plan_id`='" + str(plan_id) + "'")
    s1 = cmd.fetchall()
    return render_template('ar_view_upload_plan_more.html', d=s, v=s1)


@root.route('/button1',methods=['get','post'])
def button1():
    btn = request.form['Submit']
    if btn == "Edit":
        id=session['id']
        cmd.execute("SELECT `plan`.*,`plan_img`.`upload_img1` FROM plan JOIN`plan_img`ON`plan_img`.`plan_id`=`plan`.`plan_id` WHERE `plan`. plan_id='" + str(id) + "'")
        s = cmd.fetchone()
        cmd.execute("SELECT `upload_img1` FROM `plan_img` WHERE `plan_id`='" + str(id) + "'")
        s1 = cmd.fetchall()
        return render_template('ar_view_upload_plan_edit.html', d=s, v=s1)
    else:
        id = session['id']
        cmd.execute("DELETE FROM plan WHERE plan_id='"+str(id)+"'")
        cmd.execute("DELETE FROM plan_img WHERE plan_id ='"+str(id)+"'")
        return '''<script>alert("Deleted");window.location="/ar_view_upload_plan"</script>'''


@root.route('/ar_view_upload_plan_edit')
def ar_view_upload_plan_edit():
    return render_template('ar_view_upload_plan_edit.html')


@root.route('/ar_edit_plan_action', methods=['get', 'post'])
def ar_edit_plan_action():
    plan_id=session['id']
    print(plan_id)
    pa = request.form['textfield']
    sf = request.form['textfield2']
    rm = request.form['textfield3']
    brm = request.form['textfield4']
    st = request.form['textfield5']
    cp = request.form['textfield6']
    fa = request.form['textfield7']
    od = request.form['textarea']
    tl=request.form['textfield8']
    cmd.execute("update plan set plot_area='" + pa + "',sq_feet='" + sf + "',noof_room='" + rm + "',noof_bedroom='" + brm + "',noof_stories='" + st + "',car_parking='" + cp + "',front_area='" + fa + "',description1='" + od + "',plan_title='"+tl+"' WHERE plan_id='"+str(plan_id)+"' ")
    con.commit()
    return '''<script>alert('Updated');window.location="/ar_view_upload_plan"</script>'''


@root.route('/ar_view_upload_plan_img',methods=['get','post'])
def ar_view_upload_plan_img():
    id=request.args.get('id')
    return render_template('ar_view_upload_plan_img.html')


@root.route('/ar_view_plan_img_action',methods=['get','post'])
def ar_view_plan_img_action():
    bt1=request.form['Submit']
    if bt1=='Next':
        id=session['id']
        photo = request.files['file']
        img = secure_filename(photo.filename)
        photo.save(os.path.join(plan_path, img))
        cmd.execute("update plan_img set upload_img1='" + img + "' WHERE plan_id='"+ str(id) + "'")
        con.commit()
        return '''<script>alert("Do you want to upload the next image");window.location="/ar_view_upload_plan_img"</script>'''
    else:
        return '''<script>alert("Finished");window.location="/editimg"</script>'''


@root.route('/editimg',methods=['get','post'])
def editimg():
        id=session['id']
        cmd.execute("SELECT `plan`.*,`plan_img`.`upload_img1` FROM plan JOIN`plan_img`ON`plan_img`.`plan_id`=`plan`.`plan_id` WHERE `plan`. plan_id='" + str(id) + "'")
        s = cmd.fetchone()
        cmd.execute("SELECT `upload_img1` FROM `plan_img` WHERE `plan_id`='" + str(id) + "'")
        s1 = cmd.fetchall()
        return render_template('ar_view_upload_plan_edit.html', d=s, v=s1)


# --------------------------------------VIEW CUSTOMIZED PLANS-----------------------------------------------------------------------------------


@root.route('/ar_view_customized_plan')
def ar_view_customized_plan():
    cmd.execute("SELECT `cust_plan`.`cplan_id`,`reg_cust`.`f_name`,`l_name` FROM `reg_cust` JOIN `cust_plan` ON `cust_plan`.`cust_id`=`reg_cust`.`cust_id` WHERE `cust_plan`.`status`='pending' and cust_plan.arch_id='"+str(session['arid'])+"'")
    s = cmd.fetchall()
    return render_template('ar_view_customized_plan.html',val=s)


@root.route('/ar_view_customized_plan_more')
def ar_view_customized_plan_more():
     id = request.args.get('id')
     session['id']=id
     cmd.execute("SELECT `cust_plan`.*,`reg_cust`.`f_name`,`reg_cust`.`l_name`,`cust_plan_img`.`upload_img1` FROM `cust_plan` JOIN `reg_cust`ON `reg_cust`.`cust_id`=`cust_plan`.`cust_id`JOIN `cust_plan_img`ON`cust_plan_img`.`cplan_id`=`cust_plan`.`cplan_id` WHERE `cust_plan`.`cplan_id`='" + str(id) + "'")
     s = cmd.fetchone()
     return render_template('ar_view_customized_plan_more.html', d=s)


@root.route('/button',methods=['get','post'])
def button():
    btn=request.form['Submit']
    if btn=="Confirm":
        id=session['id']
        cmd.execute("UPDATE cust_plan SET status='confirm' WHERE cplan_id='" + str(id) + "'")
        con.commit()
        return '''<script>alert("Successfully Confirmed");window.location="/ar_view_customized_plan"</script>'''
    else:
        id = session['id']
        cmd.execute("UPDATE cust_plan SET status='reject' WHERE cplan_id='" + str(id) + "'")
        con.commit()
        return '''<script>alert("Rejected");window.location="/ar_view_customized_plan"</script>'''


# --------------------------------------VIEW BOOKING DETAILS-----------------------------------------------------------------------------------


@root.route('/ar_view_booking')
def ar_view_booking():
    cmd.execute("SELECT book.*,`reg_cust`.`f_name`,`reg_cust`.`l_name` FROM `book`JOIN`reg_cust`ON`reg_cust`.`cust_id`=`book`.`cust_id`WHERE STATUS='pending' and book.arch_des_id='" + str( session['arid']) + "'")
    s = cmd.fetchall()
    return render_template('ar_view_booking.html',val=s)


@root.route('/ar_view_booking_more')
def ar_view_booking_more():
    plid = request.args.get('id')
    session['plid']=plid
    print(plid)
    cmd.execute("SELECT plan.*,`plan_img`.`img_id`,`plan_img`.`upload_img1` FROM `plan_img` JOIN `plan` ON `plan_img`.`plan_id`=`plan`.`plan_id` WHERE `plan`.plan_id='" + str(plid) + "' AND   plan.arch_id='" + str( session['arid']) + "' GROUP BY plan_id")
    s = cmd.fetchone()
    return render_template('ar_view_booking_more.html',d=s)


@root.route('/button3',methods=['get','post'])
def button3():
    btn=request.form['Submit']
    if btn=="Confirm":
        id=session['plid']
        cmd.execute("UPDATE book SET status='confirm' WHERE plan_id='" + str(id) + "'")
        con.commit()
        return '''<script>alert("Successfully Confirmed");window.location="/ar_view_booking"</script>'''
    else:
        id = session['plid']
        cmd.execute("UPDATE book SET status='reject' WHERE plan_id='" + str(id) + "'")
        con.commit()
        return '''<script>alert("Rejected");window.location="/ar_view_booking"</script>'''


# --------------------------------------VIEW RATING-----------------------------------------------------------------------------------


@root.route('/ar_view_rating')
def ar_view_rating():
    id = request.args.get('id')
    session['id'] = id
    # cmd.execute("SELECT `rating`.*,`reg_arch`.`f_name`,`reg_arch`.`l_name`,`reg_arch`.`photo`FROM `rating`JOIN`reg_arch`ON`reg_arch`.`arch_id`=`rating`.`acc_id`UNION SELECT `rating`.*,`reg_ext`.`f_name`,`reg_ext`.`l_name`,`reg_ext`.`photo` FROM `rating`JOIN `reg_ext` ON `reg_ext`.`ext_id`=`rating`.`acc_id`")
    cmd.execute("SELECT rate FROM rating  WHERE acc_id='"+str(session['arid'])+"'")
    s = cmd.fetchone()
    return render_template('ar_view_rating.html',d=s)


#   EXTEROR

@root.route('/ex_home_page')
def ex_home_page():
    return render_template('ex_home_page.html')


# --------------------------------------UPLOAD DESIGNS-----------------------------------------------------------------------------------


@root.route('/ex_upload_design')
def ex_upload_design():
    return render_template('ex_upload_design.html')


@root.route('/ex_upload_design_action',methods=['get','post'])
def ex_upload_design_action():
    exid=session['exid']
    pa=request.form['textfield2']
    mt=request.form['textarea']
    od=request.form['textarea2']
    tl=request.form['textfield']
    cmd.execute("insert into design values(null,'"+str(exid)+"','"+pa+"','"+mt+"','"+od+"','"+tl+"','Approved')")
    id = con.insert_id()
    session['des_id'] = id
    print(id)
    con.commit()
    return '''<script>alert("Do you want to upload images");window.location="/ex_upload_design_img"</script>'''


@root.route('/ex_upload_design_img',methods=['get','post'])
def ex_upload_design_img():
    return render_template('ex_upload_design_img.html')


@root.route('/ex_upload_design_img_action',methods=['get','post'])
def ex_upload_design_img_action():
    bt1=request.form['Submit']
    if bt1=='Next':
        photo = request.files['file']
        img = secure_filename(photo.filename)
        photo.save(os.path.join(des_path, img))
        des_id = session['des_id']
        print(des_id)
        cmd.execute("insert into design_img value(null,'" + str(des_id) + "','" + img + "')")
        con.commit()
        return '''<script>alert("Do you want to upload the next image");window.location="/ex_upload_design_img"</script>'''
    else:
        return '''<script>alert("Finished");window.location="/ex_home_page"</script>'''


# --------------------------------------VIEW UPLOAD DESIGNS-----------------------------------------------------------------------------------


@root.route('/ex_view_upload_design')
def ex_view_upload_design():
        cmd.execute("SELECT `design`.`des_id`,`design`.`title`,`design_img`.`upload_img` FROM `design`JOIN`design_img`ON `design_img`.`des_id`=`design`.`des_id`WHERE `design`.`status`='Approved' AND `design`.`ext_id`='" + str(session['exid']) + "' GROUP BY `des_id`")
        s = cmd.fetchall()
        return render_template('ex_view_upload_design.html', val=s)


@root.route('/ex_view_upload_design_more')
def ex_view_upload_design_more():
        des_id = request.args.get('id')
        session['id'] = des_id
        cmd.execute("SELECT `design`.*,`design_img`.`upload_img` FROM `design`JOIN`design_img`ON `design_img`.`des_id`=`design`.`des_id` WHERE `design`.`des_id`='" + str(des_id) + "'")
        s = cmd.fetchone()
        cmd.execute("SELECT `upload_img` FROM `design_img` WHERE `des_id`='" + str(des_id) + "'")
        s1 = cmd.fetchall()
        return render_template('ex_view_upload_design_more.html', d=s, v=s1)


@root.route('/button2', methods=['get', 'post'])
def button2():
        btn = request.form['Submit']
        if btn == "Edit":
            id = session['id']
            cmd.execute("SELECT `design`.*,`design_img`.`upload_img` FROM `design`JOIN`design_img`ON `design_img`.`des_id`=`design`.`des_id` WHERE `design`.`des_id`='" + str(id) + "'")
            s = cmd.fetchone()
            cmd.execute("SELECT `upload_img` FROM `design_img` WHERE `des_id`='" + str(id) + "'")
            s1 = cmd.fetchall()
            return render_template('ex_view_upload_design_edit.html', d=s, v=s1)
        else:
            id = session['id']
            cmd.execute("DELETE FROM design WHERE des_id='" + str(id) + "'")
            cmd.execute("DELETE FROM design_img WHERE des_id ='" + str(id) + "'")
            return '''<script>alert("Deleted");window.location="/ex_view_upload_design"</script>'''


@root.route('/ex_view_upload_design_edit')
def ex_view_upload_design_edit():
        return render_template('ex_view_upload_design_edit.html')


@root.route('/ex_edit_design_action', methods=['get', 'post'])
def ex_edit_design_action():
    des_id = session['des_id']
    pa = request.form['textfield']
    mt = request.form['textarea']
    od = request.form['textarea2']
    tl = request.form['textfield2']
    cmd.execute("UPDATE design SET plot_area='"+ pa+"',meterials='"+mt+"',discription='"+od+"',title='"+tl+"' WHERE des_id='"+str(des_id)+"'")
    con.commit()
    return '''<script>alert('Updated');window.location="/ex_view_upload_design"</script>'''


@root.route('/ex_view_upload_design_img',methods=['get','post'])
def ex_view_upload_design_img():
    id=request.args.get('id')
    return render_template('ex_view_upload_design_img.html')


@root.route('/ex_view_upload_design_img_action',methods=['get','post'])
def ex_view_upload_design_img_action():
    bt1=request.form['Submit']
    if bt1=='Next':
        id=session['id']
        photo = request.files['file']
        img = secure_filename(photo.filename)
        photo.save(os.path.join(des_path, img))
        cmd.execute("update design_img set upload_img='" + img + "' WHERE des_id='"+ str(id) + "'")
        con.commit()
        return '''<script>alert("Do you want to upload the next image");window.location="/ex_view_upload_design_img"</script>'''
    else:
        return '''<script>alert("Finished");window.location="/editimg1"</script>'''


@root.route('/editimg1',methods=['get','post'])
def editimg1():
    id = session['id']
    cmd.execute("SELECT `design`.*,`design_img`.`upload_img` FROM `design`JOIN`design_img`ON `design_img`.`des_id`=`design`.`des_id` WHERE `design`.`des_id`='" + str(id) + "'")
    s = cmd.fetchone()
    cmd.execute("SELECT `upload_img` FROM `design_img` WHERE `des_id`='" + str(id) + "'")
    s1 = cmd.fetchall()
    return render_template('ex_view_upload_design_edit.html', d=s, v=s1)


# --------------------------------------VIEW CUSTOMIZED DESIGNS-----------------------------------------------------------------------------------


@root.route('/ex_view_customized_design')
def ex_view_customized_design():
    cmd.execute("SELECT `cust_design`.`cdes_id`,`reg_cust`.`f_name`,`l_name` FROM `reg_cust` JOIN `cust_design`ON`cust_design`.`cust_id`=`reg_cust`.`cust_id` WHERE `cust_design`.`status`='pending'  and cust_design.ext_id='"+str(session['exid'])+"'")
    s = cmd.fetchall()
    return render_template('ex_view_customized_design.html',val=s)


@root.route('/ex_view_customized_design_more')
def ex_view_customized_design_more():
     id = request.args.get('id')
     session['id']=id
     cmd.execute("SELECT `cust_design`.*,`reg_cust`.`f_name`,`reg_cust`.`l_name`,`cust_des_img`.`upload_img` FROM `cust_design`JOIN `reg_cust`ON `cust_design`.`cust_id`=`reg_cust`.`cust_id`JOIN `cust_des_img` ON `cust_design`.`cdes_id`=`cust_des_img`.`cdes_id` WHERE `cust_design`.`cdes_id`='" + str(id) + "'")
     s = cmd.fetchone()
     return render_template('ex_view_customized_design_more.html', d=s)


@root.route('/button5',methods=['get','post'])
def button5():
    btn=request.form['Submit']
    if btn=="Confirm":
        id=session['id']
        cmd.execute("UPDATE cust_design SET status='confirm' WHERE cdes_id='" + str(id) + "'")
        con.commit()
        return '''<script>alert("Successfully Confirmed");window.location="/ex_view_customized_design"</script>'''
    else:
        id = session['id']
        cmd.execute("UPDATE cust_design SET status='reject' WHERE cdes_id='" + str(id) + "'")
        con.commit()
        return '''<script>alert("Rejected");window.location="/ex_view_customized_design"</script>'''


# --------------------------------------VIEW BOOKING DETAILS-----------------------------------------------------------------------------------


@root.route('/ex_view_booking')
def ex_view_booking():
    cmd.execute("SELECT book.*,`reg_cust`.`f_name`,`reg_cust`.`l_name` FROM `book`JOIN`reg_cust`ON`reg_cust`.`cust_id`=`book`.`cust_id`WHERE STATUS='pending' AND book.arch_des_id='" + str( session['exid']) + "'")
    s = cmd.fetchall()
    return render_template('ex_view_booking.html',val=s)


@root.route('/ex_view_booking_more')
def ex_view_booking_more():
    desid = request.args.get('id')
    session['desid']=desid
    cmd.execute("SELECT `design`.*,`design_img`.`dimg_id`,`design_img`.`upload_img` FROM `design_img`JOIN`design`ON `design_img`.`des_id`=`design`.`des_id`WHERE `design`.des_id='" + str(desid) + "' AND   design.ext_id='" + str( session['exid']) + "' GROUP BY des_id")
    s = cmd.fetchone()
    return render_template('ex_view_booking_more.html',d=s)


@root.route('/button4',methods=['get','post'])
def button4():
    btn=request.form['Submit']
    if btn=="Confirm":
        id=session['desid']
        cmd.execute("UPDATE book SET status='confirm' WHERE design_id='" + str(id) + "'")
        con.commit()
        return '''<script>alert("Successfully Confirmed");window.location="/ex_view_booking"</script>'''
    else:
        id = session['desid']
        cmd.execute("UPDATE book SET status='reject' WHERE design_id='" + str(id) + "'")
        con.commit()
        return '''<script>alert("Rejected");window.location="/ex_view_booking"</script>'''


# --------------------------------------VIEW RATING-----------------------------------------------------------------------------------


@root.route('/ex_view_rating')
def ex_view_rating():
    id = request.args.get('id')
    session['id'] = id
    # cmd.execute("SELECT `rating`.*,`reg_arch`.`f_name`,`reg_arch`.`l_name`,`reg_arch`.`photo`FROM `rating`JOIN`reg_arch`ON`reg_arch`.`arch_id`=`rating`.`acc_id`UNION SELECT `rating`.*,`reg_ext`.`f_name`,`reg_ext`.`l_name`,`reg_ext`.`photo` FROM `rating`JOIN `reg_ext` ON `reg_ext`.`ext_id`=`rating`.`acc_id`")
    cmd.execute("SELECT rate FROM rating  WHERE acc_id='"+str(session['exid'])+"'")
    s = cmd.fetchone()
    return render_template('ex_view_rating.html',d=s)














# @root.route('/ex_upload_design')
# def ex_upload_design():
#     return render_template('ex_upload_design.html')
# @root.route('/ex_upload_design_action', methods=['get', 'post'])
# def ex_upload_design_action():
#     return '''<script>alert("Successfully Uploaded");window.location="/"</script>'''
#
#
# @root.route('/ex_view_customized_design')
# def ex_view_customized_design():
#     return render_template('ex_view_customized_design.html')
# @root.route('/ex_view_customized_design_more')
# def ex_view_customized_plan_more():
#     return render_template('ex_view_customized_design_more.html')
#
#
# @root.route('/ex_view_booking')
# def ex_view_booking():
#     return render_template('ex_view_booking.html')
# @root.route('/ex_view_booking_more')
# def ex_view_booking_more():
#     return render_template('ar_view_booking_more.html')
#
#
# @root.route('/ex_view_rating')
# def ex_view_rating():
#     return render_template('ex_view_rating.html')







@root.route('/changepass')
def changepass():
    return render_template('login2.html')


if(__name__=='__main__'):
    root.run(debug=True)



