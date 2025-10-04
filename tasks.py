from invoke import task

@task
def start(ctx):
    """Start the application."""
    ctx.run("python3 src/gameloop.py", pty=True )

@task
def test(ctx):
    """Run the test suite."""
    ctx.run("pytest src", pty=True)

@task
def lint(ctx):
    """Run the linter."""
    ctx.run("pylint src", pty=True)

@task
def format(ctx):
    """Format the code."""
    ctx.run("autopep8 --in-place --recursive src", pty=True)

@task
def coverage(ctx):
    """Run tests with coverage."""
    ctx.run("coverage run -m pytest src && coverage report -m && coverage html", pty=True)