		
		def show(self, option):
			if option in ["SSIDS"]:
				self.SSIDS()
				self.main()
			elif option in ["AP_MAC"]:
				self.AP_MAC()
				self.main()
			elif option in ["Vendor"]:
				self.Vendor()
				self.main()
			elif option in ["Clients"]:
				self.Clients()
				self.main()
			elif option in ["usernames"]:
				self.usernames()
				self.main()

		def main(self, choice):
			try:
				results = []
				choice()
					clrdb = qr.drop_duplicates()
					tr = clrdb.values
					for r in tr:
						if r not in results:
							results.append(r)
							print str(r)[1:-1].replace('u','').replace('\'', '')
			except pandas.io.sql.DatabaseError:
				continue


		def SSIDS(self):
			for tb in tables[0:3]:
				qr = dp.read_sql('select essid from '+ tb +'', t)

		def AP_MAC(self):
			for tb in tables[0][2]:
				qr = dp.read_sql('select bssid from '+ tb +'', t)

		def Vendor(self):			
			for tb in tables[0:3]:
				qr = dp.read_sql('select vendor from '+ tb +'', t)

		def Clients(self):
			for tb in tables[0:3]:
				qr = dp.read_sql('select client from '+ tb +'', t)

		def usernames(self):
			qr = dp.read_sql('select username from EAP', t)
