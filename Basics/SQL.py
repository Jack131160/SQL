#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3 as db

# Connect to a database (or create one if it doesn't exist)
conn = db.connect('example.db')


# In[2]:


# Create a 'cursor' for executing commands
c = conn.cursor()


# In[3]:


# If this is not the first time you run this cell, 
# you need to delete the existed "Students" table first
c.execute("DROP TABLE IF EXISTS Students")

# create a table named "Students" with 2 columns: "gtid" and "name".
# the type for column "gtid" is integer and for "name" is text. 
c.execute("CREATE TABLE Students (gtid INTEGER, name TEXT)")


# In[4]:


c.execute("INSERT INTO Students VALUES (123, 'DAN')")
c.execute("INSERT INTO Students VALUES (456, 'POO')")
c.execute("INSERT INTO Students VALUES (381, 'PIHU')")
c.execute("INSERT INTO Students VALUES (991, 'BHU')")


# In[5]:


conn.commit()


# In[6]:


# An important (and secure!) idiom
more_students = [(723, 'Rozga'),
                 (882, 'Zha'),
                 (401, 'Park'),
                 (377, 'Vetter'),
                 (904, 'Brown')]

# '?' question marks are placeholders for the two columns in Students table
c.executemany('INSERT INTO Students VALUES (?, ?)', more_students)
conn.commit()


# In[7]:


c.execute("SELECT * FROM Students")
results = c.fetchall()
print("Your results:", len(results), "\nThe entries of Students:\n", results)


# In[8]:


c.execute('DROP TABLE IF EXISTS Takes')
c.execute('CREATE TABLE Takes (gtid INTEGER, course TEXT, grade REAL)')


# In[9]:


grades = [(123,"CSE 6040",4.0),(123,"ISYE 6644",3.0),(123,"MGMT 8803",1.0),
          (991,"CSE 6040",4.0),(991,"ISYE 6740",4.0),
          (456,"CSE 6040",4.0),(456,"ISYE 6740",2.0),(456,"MGMT 8803",3.0)]


# In[10]:


# '?' question marks are placeholders for the two columns in Students table
c.executemany('INSERT INTO Takes VALUES (?, ?,?)', grades)
# Displays the results of your code
c.execute('SELECT * FROM Takes')
results = c.fetchall()
print("Your results:", len(results), "\nThe entries of Takes:", results)
conn.commit()


# In[11]:


# Test cell: `insert_many__test`

# Close the database and reopen it
conn.close()
conn = db.connect('example.db')
c = conn.cursor()
c.execute('SELECT * FROM Takes')
results = c.fetchall()

if len(results) == 0:
    print("*** No matching records. Did you remember to commit the results? ***")
assert len(results) == 8, "The `Takes` table has {} when it should have {}.".format(len(results), 8)

assert (123, 'CSE 6040', 4.0) in results
assert (123, 'ISYE 6644', 3.0) in results
assert (123, 'MGMT 8803', 1.0) in results
assert (991, 'CSE 6040', 4.0) in results
assert (991, 'ISYE 6740', 4.0) in results
assert (456, 'CSE 6040', 4.0) in results
assert (456, 'ISYE 6740', 2.0) in results
assert (456, 'MGMT 8803', 3.0) in results

print("\n(Passed.)")


# In[12]:


# See all (name, course, grade) tuples
query = '''
        SELECT Students.name, Takes.course, Takes.grade
        FROM Students, Takes
        WHERE Students.gtid = Takes.gtid
'''

for match in c.execute(query): # Note this alternative idiom for iterating over query results
    print(match)


# In[13]:


# Define `query` with your query:
query = '''
        SELECT Students.name, Takes.grade
        FROM Students, Takes
        WHERE Students.gtid = Takes.gtid
        AND Takes.course="CSE 6040"
'''

c.execute(query)
results1 = c.fetchall()
results1


# In[14]:


# Define `query` string here:

query = '''
        SELECT Students.name, Takes.grade
        FROM Students
        LEFT OUTER JOIN Takes on Students.gtid = Takes.gtid
        
'''


# Executes your `query` string:
c.execute(query)
matches = c.fetchall()
for i, match in enumerate(matches):
    print(i, "->", match)


# In[15]:


query = '''
        SELECT gtid, AVG(grade)
        FROM Takes 
        GROUP BY gtid
'''

for match in c.execute(query):
    print(match)


# In[16]:


c.close()
conn.close()


# In[ ]:




