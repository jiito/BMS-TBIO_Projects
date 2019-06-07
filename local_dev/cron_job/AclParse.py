# this is a script designed to parse ACLs using the linux commands getfacl and setfacl
class AclParse:
    
    # import library
    import subprocess

    user = ""
    user_groups_total = []
    user_group = ""
    
    named_groups = []

    owner = ""
    group = ""

    group_perms = {}
    user_perms = {}
    aces = {}

    # run the getfacl commands on a file
    def getACE(self, file, user):

        self.user = user
        self.setGroups()

        # set command to get the ACL 
        cmd = ["getfacl", file]
        
        acl = str(self.subprocess.check_output(cmd))

        # process ACLs
        acl = acl.split("\n")
        aces = {}

        owner = acl[1].strip(' #').split()[1]
        self.setOwner(owner)
        group = acl[2].strip(' #').split()[1]
        self.setGroup(group)
        #print(owner)
        #print(group)

        for line in acl[3:len(acl)-2]: # get owner and user perm
            line = line.strip(' #')
            line = line.replace("::", ":all:")
            ace = line.split(':')
            #print(ace)
            
            #print(line)

            if ace[0] == "group":
                self.group_perms[ace[1]] = ace[2]
            elif ace[0] == "user":
                self.user_perms[ace[1]] = ace[2]
            else:
                aces[ace[0]] = ace[2]
        
        #update ACEs
        aces["groups"] = self.group_perms
        aces["users"] = self.user_perms
        #print(self.group_perms)
        #print(self.user_perms)
        
        #print(self.user)
        #print(self.owner)
       
        self.aces = aces
        
        self.setNamedGroups()
        print("SGN:")
        print(self.named_groups)
        #print(aces)
        #print(self.user_groups_total)
        #algorithm 
        

    def getPerm(self, file, user):
        
        #generate ACEs
        self.getACE(file, user)

        if self.checkOwner():
            print("IS OWNER")
            return self.aces["users"]["all"]
        elif self.checkUserNamed():
            print("User NAMED")
            return self.applyMask(self.aces["users"][self.user])
        elif self.checkGroupOwned():
            print("IS IN OWNING GROUP")
            return self.aces["groups"]["all"]
        elif self.checkGroupNamed():
            perms = self.applyUnion() # get union of all group permissions
            return self.applyMask(perms)
        else:
            print("IS OTHER")
            return self.aces["other"]

       # return ace
    
    def applyMask(self, perms):
        u_perms = perms
        mask = self.aces["mask"]
        perm = ""
        for i in range(3):
            if u_perms[i] != mask[i]:
                perm += '-'
            else:
                perm += u_perms[i]
        return perm

    def applyUnion(self):
        perm = ""
        l = ['r', 'w', 'x']
        for j in range(len(self.named_groups)-1):
            print(j)
            perm1 = self.aces["groups"][self.named_groups[j]]
            perm2 = self.aces["groups"][self.named_groups[j+1]]
            for i in range(3):
                print(self.named_groups[j][i])                
                if perm1[i] != perm2[i]:
                    perm += l[i]
                else:
                    perm += perm1[i]
        print("UNION of PERMS is:" + perm)
        return perm 

    # SETTERS and CHECKERS
    def setOwner(self, user):
        self.owner = user
    
    def setGroup(self, g):
        self.group = g
  
    def checkOwner(self):
        return self.user == self.owner
    
    def checkUserNamed(self):
        return self.user in self.aces["users"]
   
    def setNamedGroups(self):
        for group in self.user_groups_total:
            #print(group)
            if group in self.aces["groups"]:
                self.named_groups.append(group)
                continue
            else:
                continue
        
    def checkGroupNamed(self):
        return len(self.named_groups) >= 1

    def checkGroupOwned(self):
        for group in self.user_groups_total:
            #print(group)
            if group == self.group:
                self.user_group = group
                return True
            else:
                continue
        return False

    def setGroups(self):
        cmd = ["groups", self.user]
        self.user_groups_total = self.subprocess.check_output(cmd).split()[2:]
    
    def checkPermFile(self, file, user, perm):
        ace = self.getPerm(file, user)

        if ace[perm] == "-":
            return(False)
        else:
            return(True)

    # run getfacl on directory
    def checkPermDir(self, dir, user):
        ace = self.getPerm(dir, user)

        if ace[0] != "r" and ace[2] != "x":
            return(0)
        if ace[2] != "x":
            return(1)
        if ace[0] != "r":
            return(2)
        else:
            return(3)

