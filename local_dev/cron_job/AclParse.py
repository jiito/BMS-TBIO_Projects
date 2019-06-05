# this is a script designed to parse ACLs using the linux commands getfacl and setfacl
class AclParse:
    
    # import library
    import subprocess

    # run the getfacl commands on a file
    def getUserACE(self, file, user):
        cmd = ["getfacl", file, "--tabular"]
        
        acl = self.subprocess.check_output(cmd)
        
        u_index = acl.find(user)

        #parse the user's ACE from the output
        u_index += len(user)+2
        ace = acl[u_index:u_index + 5]
        print(ace)
        return ace

    def checkPerm(self, file, user, perm):
        ace = self.getUserACE(file, user)

        if ace[perm] == "-":
            return(False)
        else:
            return(True)
