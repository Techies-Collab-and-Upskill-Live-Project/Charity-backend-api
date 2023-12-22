# CharityDonate

### 🧑🏽‍💻 Here is a workflow to contribute to projects.

1. Clone this repository to your local machine.

```
git clone [this-repo]
```

2. Change to the repository directory on your computer:

```
cd CHARITYDONATE
```

4. Create a branch using the `git switch` command:

```bash
git switch -c branch-name
```

5. Create your virtual environment(Linux OS)

```bash
python3 -m venv venv; source venv/bin/activate
```

6. Install all Packages in requirements

```bash
pip install -r requirements.txt
```

7. Install all Packages in requirements

```bash
pip install -r requirements.txt
```

8. Run Migration

```bash
python3 manage.py makemigrations; python3 manage.py migrate
```

9. Run Server ensure that is no error, if there is(are) errors, fix them before pushing

```bash
python3 manage.py runserver
```

10. Implementing your features
    if you install a new packge, add to the requirements file using this

```bash
pip freeze > requirements.txt
```

11. Push to your branch(not main branch)

```bash
git push origin  branch-name
```

12. Then Come to Github to make pull request
