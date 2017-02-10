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

def cds_polito(fname):
    """
    get the Names of the Departments at polito
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
    def __init__(self, mainDir, csv_filename, cds_filename):
        filename = os.path.join(mainDir, csv_filename)
        self.students = pd.read_csv(filename, index_col=0)
        self.surnames = list(self.students['COGNOME'])
        self._id_codes = list(self.students.index)
        self._cds_polito = cds_polito(os.path.join(mainDir, cds_filename))
        
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
            df = self.students[self.students['COGNOME'] == surname]
            return df
        else:
            print("Surname %s not in the list" % surname)
            return None
        # Can be done with try ... except ...

    def _get_student_info_by_id(self, id_code):
        """
        returns a pandas dataframe
        with the students' info
        based on id_code (Matricola)
        """
        return self.students.loc[id_code]

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


    def get_students_cds(self, cds):
        cds_short = cds[:3]
        cds_long = self._cds_polito[cds_short]
        locations = self.students['CDS STUDENTE'] == cds
        st = sum(locations)
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
        df = self._get_student_info(tag)
        code = df.index.tolist()[0]
        try: 
            url = "https://didattica.polito.it/pls/portal30/sviluppo.foto_studente?p_matricola=%s" % code
            response = requests.get(url)
            cnt = response.content
            img = Image.open(BytesIO(cnt))
        except OSError:
            cnt = cnt.decode("utf-8")
            if 'ACCESS DENIED' in cnt:
                 webbrowser.open(url)
        except:
            print("Impossible to connect to the Polito site")

    @property
    def cds(self):
        return set(self.students['CDS STUDENTE'])

if __name__ == "__main__":
    mainDir = "/home/gf/src/Python/Python-in-the-lab/project"
    csv_file = "01RONKG_2017.csv"
    cds_file ='phds.txt'
    filename = os.path.join(mainDir, csv_file)
    cl = Classroom(mainDir, csv_file, cds_file)
    for c in sorted(cl.cds):
        cl.get_students_cds(c)