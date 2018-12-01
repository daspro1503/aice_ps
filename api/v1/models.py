import re
import datetime
class ireporter(object):
    
    def __init__(self):
        self.users=[]
        self.incident=[]
        self.id=""
        self.default_admin="admin1234"
    def signup(self,fname,sname,oname,email,phonenumber,username,password):
        
        exists1=False
        exists_phone_number=False
        exists_email=False
        match = re.match( '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$' ,email)
        if username=="" or password=="":
            return {"status":"401","Data":"username or password is missing please enter the missing details and try again"}
        
        elif fname=="":
            return {"status":"401","Data":"first name is missing please enter the missing details and try again"}
        elif phonenumber=="":
            return {"status":"401","Data":"Phone number is missing please enter the missing details and try again"}
        elif match==None:
            return {"status":"401","Data":"Email entered is invalid please enter a valid email and try again"}
        else:
            if username!=self.default_admin or password!=self.default_admin:
                isAdmin=False
            elif username==self.default_admin and password==self.default_admin:
                isAdmin=True
            for user_dict in self.users:
                for keys,value in user_dict.items():
                    if user_dict['username']==username:
                        return {"status":"401","Data":"Username already in use please try another username"}
                        exists1=True
                        break
                break
                
            if exists1==False:
                for user_dict in self.users:
                    for keys,value in user_dict.items():
                        if user_dict['phonenumber']==phonenumber:
                            return {"status":"401","Data":"Phone number already registered please use another phone number"}
                            exists_phone_number=True
                            break
                    break
            if exists_phone_number==False:
                 for user_dict in self.users:
                    for keys,value in user_dict.items():
                        if user_dict['email']==email:
                            return {"status":"401","Data":"Email already registered please use another email and try again"}
                            exists_email=True
                            break
                    break
 
            if exists_email==False:
               self.id=len(self.users)+1
               user={"id":self.id,"firstname":fname,"lastname":sname,"othername":oname,"email":email,"phonenumber":phonenumber,"username":username,"password":password,"isAdmin":isAdmin}
               self.users.append(dict(user)) 
               return {"status":"201","Data":[user]}      


            
    def create_incident(self,CreatedBy,i_type,location,images,videos,comment):

        i_type=i_type.lower()
        registered_user=False  
        createOn=datetime.date.today()
        
        for user_dict in self.users:
            for keys,value in user_dict.items():
                if user_dict['username']==CreatedBy:
                    registered_user=True
                    break
            break
        if registered_user==False:
            return {"status":"401","Data":"CreatedBy contains an unknown user please enter a valid username and try again"}
        if registered_user==True:
            if comment=="":
                return {"status":"401","Data":"Please enter the details of the incident and try again"}
            elif i_type=="" or i_type!="redflag":
                return {"status":"401","Data":"please enter a valid type of the incident and try again"}
            else:

                self.id=len(self.incident)+1
                incident_record={"id":self.id,"createdOn" :createOn,"createdBy":CreatedBy,"type":i_type,"location":location,"status":"unresolved","images":images,"videos":videos,"comment":comment}    
                self.incident.append(dict(incident_record))
                return {"status":"201","Data":[incident_record]}
        
    def get_all(self,CreatedBy):
        registered_user=False
        records_dict=[]
        for user_dict in self.users:
            for keys,value in user_dict.items():
                if user_dict['username']==CreatedBy:
                    registered_user=True
                    break
            break
        if registered_user==False:
            return{"status":"401","Data":"CreatedBy contains an unknown user please enter a valid username and try again"}
        if registered_user==True:
            for user_dict in self.incident:
                for keys,value in user_dict.items():
                    if user_dict['createdBy']==CreatedBy:
                        records_dict.append(dict(user_dict))
                        break
            return {"status":"200","Data":[records_dict]}

            
        
    def get_all_admin(self,username):
        record_changed=False
        registered_user=False
        for user_dict in self.users:
            for keys,value in user_dict.items():
                if user_dict['isAdmin']==True and user_dict['username']==username:
                    registered_user=True
                    break
            break
        if registered_user==False:
            return {"status":"401","Data":"CreatedBy contains an unknown user please enter a valid username and try again"}
        if registered_user==True:
            return self.incident
    def patch_record(self,id,rtype,value):
        records_exists=False
        for user_dict in self.incident:
            for keys,value in user_dict.items():
                if  user_dict['id']==id:
                    records_exists=True
                    if records_exists==True:
                        if user_dict['status']=="resolved": 
                            return "The redflag can not be edited because it has been already resolved"  
                        if user_dict['status']=="rejected":
                            return"The redflag can not be edited because it is already rejected "
                        if rtype=="location":
                            user_dict['location']=value
                            record_changed=True
                            msg="updated red flag's location"
                        if rtype=="images":
                            user_dict[images]=value
                            record_changed=True
                            msg="upated red flag's images"
                        if rtype=="videos":
                            user_dict['videos']=value
                            record_changed=True
                            msg="updated red flag's videos"
                        if rtype=="comment":
                            user_dict['comment']!=value
                            record_changed=True
                            msg="updated red flag 's comment"
                        if record_changed==True:
                            return [{'id':id,'data':msg}]
                    
              
        if records_exists==False:
            return "The id entered does not have a matching record enter another record id and try again"
    def delete_record(self,id):
        records_exists=False
        for user_dict in self.incident:
            for keys,value in user_dict.items():
                if  user_dict['id']==id:
                    records_exists=True
                    if records_exists==True:
                        self.incident.remove(user_dict)
                        return"record deleted succesfully"
                        break                    
        if records_exists==False:
            return "The id entered does not have a matching record enter another record id and try again"           
    def reject_record(id,name):
        pass
    def resolve_record(id,name):
        pass

    
#test=ireporter()
#print(test.signup("jemba","david","gerald","jembadavid45@gmail.com","07889798798","daspro1503","1234","ads"))