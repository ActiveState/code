 class Class_Ip :
... 	def __init__(self):
... 		self.listeip =[]
... 	def saisie(self):
... 		i=0
... 		while i< 4 :
... 			self.val =raw_input("entrer l adresse ip svp")
... 			self.listeip.append(self.val)
... 			i +=1
... 	def affiche(self):
... 		return ".".join(self.listeip)
... 	        print ("l adresse ip saisie est:")
... 	        print self.listeip
... 	def classe_ip(self):
... 		self.li = int(self.listeip[0])
... 		if self.li <=127 :
... 			print("la classe de l adresse ip est: A")
... 		elif self.li >=128 and self.li <=191: 
... 			print("la classe de l adresse ip est: B")
... 		elif  self.li >=192 and self.li <=223 :
... 			print("la classe de l adresse ip est: C")
... 		elif self.li >=224 and self.li <=239 :
... 			print("la classe de l adresse ip est: D")
... 		elif self.li >=240 and self.li <=255 :
... 			print("la classe de l adresse ip est: E")
... 	def binaire(self):
... 		self.listebinaire = []
... 		j=0
... 		while j<4:
... 			self.listebinaire.append(bin(int(self.listeip[j])))
... 			j +=1
... 		return ".".join(self.listebinaire)
... 	        
