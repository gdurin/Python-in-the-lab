"""
Script to load info
of students from a cvs database
"""
import os
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import webbrowser
import matplotlib.pylab as plt
import numpy as np

def cds_polito(fname):
    """
    get the Names of the Departments at Politecnico
    given as short name, long name
    """
    cds = dict()
    with open(fname) as f:
        data = f.readlines()
    for row in data:
        # Split only using the first comma
        s, l = row.split(",", 1)
        # Populate the dict
        cds[s] = l.strip() # Clean the spaces
    return cds

class Classroom:
    """
    class to load a csv file
    containing a table of students
    
    It is a combination of semi-private methods like
    _get_student_info_by_*
    and a public one 
        get_student_info(tag)
    which accepts a tag as a number (id_code, matricola)
    and as a string (surname)
    """
    def __init__(self, csv_filename, cds_filename, cols=6):
        self.students = pd.read_csv(csv_filename, index_col=0, usecols=range(cols))
        self.surnames = list(self.students.COGNOME)
        self._id_codes = list(self.students.index)
        self._cds_polito = cds_polito(cds_filename)
        
    def _get_student_info_by_surname(self, surname):
        """
        returns a pandas dataframe
        with the students' infos
        based on the surname
        """
        # Surname are saves as Capital, so let's transform
        surname = surname.upper()
        if surname in self.surnames:
            # extract the student as a dataframe of pandas
            df = self.students[self.students.COGNOME == surname]
            return df
        else:
            print("Surname %s not in the list" % surname)
            return None
        # Can be done with try ... except ...

    def _get_student_info_by_id(self, id_code):
        """
        returns a pandas dataframe
        with the student' info
        based on id_code (Matricola)
        """
        # Problem1: trap the error if the id_code does not exist
        # Problem2: use a fuzzy logic to give me back the closest number
        # considering a digit of difference (i.e.) 123456 vs 113456
        assert len(str(id_code)) == 6
        try:
            q = self.students.loc[id_code]
            return q
        except KeyError as e:
            print(e)
            scores = [self._compare_strings(id_code, code) for code in self._id_codes]
            if min(scores) == 1:
                loc_min = np.argmin(scores)
                q = input("Did you mean: %i (Y/n)? " % self._id_codes[loc_min])
                if q.upper() == "Y":
                    return self.students.iloc[loc_min]

        # except KeyError:
        #     closest_id=self.students.index[np.searchsorted(self.students.index,id_code)-1]
        #     print('Error: student id not found \nPerhaps you mean %s?' % (closest_id))
        #     return self._get_student_info_by_id(closest_id)


    def _compare_strings(self, s1, s2):
        if not isinstance(s1, str):
            s1 = str(s1)
        if not isinstance(s2, str):
            s2 = str(s2)
        score = sum([e1!=e2 for e1, e2 in zip(s1, s2)])
        return score


    def _get_student_info(self, tag=None):
        if not tag:
            print("Please give a id code or his/her surname")
            return
        else:
            return self._get_df_from_tag(tag)

    def get_student_info(self, tag=None):
        """
        Why two methods with the same name
        just one private?
        If we return a dataframe,
        pandas will plot it, 
        and this is what we do not want to
        """
        df = self._get_student_info(tag)
        if df is not None:
            print(df.to_string())
        return

    def _get_df_from_tag(self, tag):
        """
        get the pandas dataframe
        corresponding a tag (id_code or surname)

        tag: int or string (also as 'ALL')
        """
        if type(tag) == int and tag in self._id_codes:
            df = self._get_student_info_by_id(tag)
        elif type(tag) == str:
            tag = tag.upper() 
            if tag in self.surnames:
                df = self._get_student_info_by_surname(tag)
            elif tag == 'ALL':
                df = self.students
            else:
                df = None
                print("%s surname does not exist" % tag)
        else:
            print("There is a problem, check your input")
            df = None
        return df

    def get_students_cds(self, cds, is_print=True):
        cds_short = cds[:3]
        cds_long = self._cds_polito[cds_short]
        locations = self.students['CDS STUDENTE'] == cds
        st = sum(locations)
        if is_print:
            # Can we adjust plural and singular?
            if st == 1:
                verb, stud = "is", ""
            else:
                verb, stud = "are", "s"
            print("There %s %i student%s from %s" % (verb, st, stud, cds_long))
        return st

    def get_student_photo(self, tag=None):
        """
        This method unfortunately works
        only if connected to the polito network
        """
        if not tag:
            print("Please provide some info")
            return
        df = self._get_student_info(tag)
        url = "https://didattica.polito.it/pls/portal30/sviluppo.foto_studente?p_matricola=%s" % df.name
        webbrowser.open(url)
        print("Browser opened")
        
    @property
    def cds(self):
        return set(self.students['CDS STUDENTE'])

class WinterClassroom(Classroom):
    def __init__(self, csv_filename, cds_filename, cols=6):
        Classroom.__init__(self, csv_filename, cds_filename, cols=6)
        is_winter = self.students.FREQUENZA == 'Winter'
        self.students = self.students[is_winter]
        self.surnames = list(self.students.COGNOME)
        self._id_codes = list(self.students.index)

    def plot_pie(self, cdsName=None, group=1):
        if group==1:
            self.plot_pie_g1(cdsName)
        elif group==6:
            self.plot_pie_g6(cdsName)


    def plot_pie_g1(self, cdsName=None):
        """
        plot the distribution of CDS students in a pie
        see matplotlib documentation
        """
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = [cds[:3] for cds in self.cds]
        sizes = [self.get_students_cds(code) for code in self.cds]
        fig1, ax1 = plt.subplots()
        # if cdsName != None or cdsName in self.cds:
        #     explode = []
        #     for a in self.cds:
        #         if a == cdsName:
        #             explode.append(0.2)
        #         else:
        #             explode.append(0)

        #     ax1.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%',
        #             shadow=True, startangle=90)
        # else:
        #     ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        #         shadow=True, startangle=90)
        # End of original code
        explode = [0.2*(cdsName==cds) for cds in self.cds]
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', explode=explode,
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    def plot_pie_g6(self, cdsName=None):
        # No need to redifine the self.get_student_cds
        # Just add a bool to print out the number (see above)
        # labels = self.cds
        # labels_short,sizes,explodes = [], [], []
        # for label in labels:
        #     size = self.get_students_cds(label, is_print=False) # See the change here
        #     label_short = label[:3]
        #     if label == 'FISRT9':
        #         explode = 0.1
        #     else:
        #         explode = 0.0
        #     labels_short.append(label_short)
        #     explodes.append(explode)
        #     sizes.append(size)
        sizes = [self.get_students_cds(label, is_print=False) for label in self.cds]
        labels_short = [cds[:3] for cds in self.cds]
        explodes = [0.1*(cdsName==cds) for cds in self.cds]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels_short, explode=explodes, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        plt.show()


    def plot_bar(self, group=2):
        """
        plot the distribution of CDS students in a bar
        see matplotlib documentation
        """
        if group==2:
            x = [self.get_students_cds(code) for code in self.cds]
            label = list(self.cds)
            #print ('This is x: \n')
            plt.figure(figsize=(12, 5))
            plt.bar(label, x)
        elif group==7:
            #list_cds = [i for i in self.cds]
            list_4bar = []
            for element in self.cds: 
                list_4bar.append(len(self.students[self.students["CDS STUDENTE"] == element]))
            ind = np.arange(len(list_4bar), step=1)
            fig, ax = plt.subplots()
            width = 0.75
            ax.set_axisbelow(True)
            ax.grid(linestyle='--')
            ax.barh(ind, list_4bar, width, color='rgbcmykw', edgecolor='k')
            # x = list_cds
            # y = list_4bar
            ax.set_yticks(ind)
            ax.set_yticklabels(self.cds, minor=False)
            myticks = np.arange(0, max(list_4bar) + 2, step=1)
            ax.set_xticks(myticks)
            plt.xlabel('Students for CDS')
            plt.ylabel('CDS')
            plt.title('CDS of Winter session')
            for i, v in enumerate(list_4bar):
                ax.text(v + 0.15, i, str(v), color='black', va='center', fontweight='bold') 
            plt.show()

    def write_emails(self, use='id_code'):
        """
        write a students_emails.txt file with as
        <Surname Name> email;
        etc
        """
        # My solution
        if use == 'id_code':
            with open("students_emails.txt", 'w') as f:
                for c,n,id_code in zip(self.students.COGNOME, self.students.NOME, 
                                self.students.index): 
                    f.write("'%s %s' <S%s@studenti.polito.it>;" % (c,n,id_code))
            print("Student_emails.txt written")     
        # Solution group 8
        elif use == 'surnames':
            emails=[]
            with open('students_emails.txt', 'w') as f:
                for index in self.students.index:
                    email = "%s.%s@polito.it" % ((self.students.NOME[index].lower()).split()[0], 
                        (self.students.COGNOME[index].lower()).split()[0])
                    print(email, file=f)
        

    def write_cds_id_sorted(self, file_out="students_ids.txt"):
        """
        write a students_ids.txt file with as
        ***** cds1 ******
        id1 Surname1 Name1
        id2 Surname2 Name2
        .... 
        ***** cds2 ******
        idx Surnamex Namex
        etc
        with cds and Surnames sorted
        """
        # From group 9
        with open(file_out,"w+") as f:
        #cds_set=self.cds
            for c in self.cds:
                group = self.students[self.students['CDS STUDENTE'] == c]
                gi = list(group.index) # No need to make a set
                # gi = group.index.values
                f.write("***** %s *****\r\n"%c)
                for _student in gi:
                    student_info = self._get_student_info(_student)
                    f.write("%d %s %s\r\n"%(_student, ST.COGNOME, ST.NOME))

    def write_cds_surnames_sorted(self, outfile="cds_surname_sorted.txt"):
        """
        write a students_surnames.txt file with as
        ***** cds1 ******
        Surname1 Name1 id1
        Surname2 Name2 id2
        .... 
        ***** cds2 ******
        Surnamex Namex idx
        etc
        with cds and Surnames sorted
        """
        # from group 5
        f = open(outfile, "w")

        my_dict = self.students.groupby(['CDS STUDENTE'], sort = True).groups   #mi restituisce una toupla = dizionario
                                                                                #La chiave è il CDS che resituisce le matricole che sono le chiavi del database
        for i, j in my_dict.items():
            f.write("\n******%s******\n" %i)
            for mat in j:
                stud = self.students.loc[mat]
                f.write("{0} {1} {2}\n".format(stud.NOME, stud.COGNOME,mat))
        f.close()
        # A better solution
        groups = self.students.groupby(['CDS STUDENTE'], sort=True)
        for cds, df in groups:
            print("{0}{1}{0}".format(5*"*", cds))
            for n,c,mat in zip(df.NOME, df.COGNOME, df.index):
                print("{0} {1} {2}".format(n,c,mat))
            print()

if __name__ == "__main__":
    csv_file = "01RONKG_2019.csv"
    cds_file ='phds.txt'
    cl = WinterClassroom(csv_file, cds_file)
    for c in sorted(cl.cds):
        cl.get_students_cds(c)