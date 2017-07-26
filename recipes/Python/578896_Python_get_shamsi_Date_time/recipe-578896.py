# Generate by Hassan Sajedi
import datetime

class IranDateTime:
    def todayShamsi_DT(self):
        dt = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        s = self.Shamsi(int(dt[6:10]), int(dt[0:2]), int(dt[3:5]))
        return (s + '  ' + dt[11:19].__str__())

    def todayShamsi(self):
        dt = datetime.datetime.now().strftime("%m/%d/%Y")
        return self.Shamsi(int(dt[6:10]), int(dt[0:2]), int(dt[3:5]))

    def Shamsi(self, Y , M , D):
        if (Y == 0):
            Y = 2000;
        if (Y < 100):
            Y = Y + 1900;
        if (Y == 2000):
            if (M > 2):
                curentDateandTime = datetime.datetime.now().strftime("%m/%d/%Y")
                year = curentDateandTime.substring(0, 4)
                month = curentDateandTime.substring(4, 6)
                day = curentDateandTime.substring(6, 8)
                Y = year
                M = month
                D = day
        if (M < 3 or (M == 3 and D < 21)):
            Y = Y - 622
        else:
            Y = (int(Y) - 621).__str__()
        if(M == 1):
            if (D < 21):
                M = 10
                D = D + 10
            else:
                M = 11
                D = D - 20
        elif(M == 2):
            if (D < 20):
                M = 11
                D = D + 11
            else:
                M = 12
                D = D - 19
        elif(M == 3):
            if (D < 21):
                M = 12;
                D = D + 9;
            else:
                M = 1;
                D = D - 20;
        elif (M == 4):
            if (D < 21):
                M = 1;
                D = D + 11;
            else:
                M = 2;
                D = D - 20;
        elif (M == 5):
            if (D < 22):
                M = M - 3;
                D = D + 10;
            else:
                M = M - 2;
                D = D - 21;
        elif (M == 6):
            if (D < 22):
                M = M - 3;
                D = D + 10;
            else:
                M = M - 2;
                D = D - 21;
        elif (M == 7):
            if (D < 23):
                M = M - 3;
                D = D + 9;
            else:
                M = M - 2;
                D = D - 22;
        elif (M == 8):
            if (D < 23):
                M = M - 3;
                D = D + 9;
            else:
                M = M - 2;
                D = D - 22;
        elif (M == 9):
            if (D < 23):
                M = M - 3;
                D = D + 9;
            else:
                M = M - 2;
                D = D - 22;
        elif (M == 10):
            if (D < 23):
                M = 7;
                D = D + 8;
            else:
                M = 8;
                D = D - 22;
        elif (M == 11):
            if (D < 22):
                M = M - 3;
                D = D + 9;
            else:
                M = M - 2;
                D = D - 21;
        elif (M == 12):
            if (D < 22):
                M = M - 3;
                D = D + 9;
            else:
                M = M - 2;
                D = D - 21;
        month = "00";
        day = "00";
        D = int(D);
        if (M < 10):
            month = "0" + str(M);
        else:
            month = str(M);
        if (D < 10):
            day = "0" + str(D);
        else:
            day = str(D);
        return str(Y) + "/" + month + "/" + day;
