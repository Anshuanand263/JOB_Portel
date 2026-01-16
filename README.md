<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Job Portal Backend – Flask & MongoDB</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>Job Portal Backend</h1>
<h3>Flask + MongoDB Based Web Application Backend</h3>

<p>
This repository contains the backend implementation of a <b>Job Portal Web Application</b>
developed using <b>Flask</b> and <b>MongoDB</b>. The backend handles authentication,
role-based access (users and job providers), job postings, job applications,
and session management.
</p>

<hr>

<h2>Backend Responsibilities</h2>
<ul>
    <li>User and Provider registration & authentication</li>
    <li>Password hashing and secure login</li>
    <li>Role-based routing (Job Seeker / Job Provider)</li>
    <li>Job posting and management</li>
    <li>Job search and filtering</li>
    <li>Job application handling</li>
    <li>Session-based access control</li>
</ul>

<hr>

<h2> Technologies Used</h2>
<ul>
    <li><b>Backend Framework:</b> Flask (Python)</li>
    <li><b>Database:</b> MongoDB</li>
    <li><b>ODM / Driver:</b> PyMongo</li>
    <li><b>Authentication:</b> Werkzeug Password Hashing</li>
    <li><b>Session Management:</b> Flask Sessions</li>
</ul>

<hr>

<h2> Database Collections</h2>
<ul>
    <li><b>users</b> – Job seekers</li>
    <li><b>providers</b> – Job providers / companies</li>
    <li><b>job_collections</b> – Job postings</li>
    <li><b>applicants_col</b> – Job applications</li>
</ul>

<hr>

<h2> Authentication & Authorization</h2>
<ul>
    <li>Passwords are stored using secure hashing</li>
    <li>Separate login flow for users and providers</li>
    <li>Session-based authentication</li>
    <li>Protected routes redirect unauthorized users to login</li>
</ul>

<hr>

<h2> Backend Workflow</h2>
<ol>
    <li>User or provider registers with role selection</li>
    <li>Password is hashed and stored in MongoDB</li>
    <li>User logs in and session is created</li>
    <li>Providers can post and manage jobs</li>
    <li>Users can search, view, and apply for jobs</li>
    <li>Applications are stored and visible to providers</li>
</ol>

<hr>

<h2>API Routes Overview</h2>
<ul>
    <li><b>/register</b> – User / Provider registration</li>
    <li><b>/</b> – Login</li>
    <li><b>/home</b> – User dashboard</li>
    <li><b>/providers/home</b> – Provider dashboard</li>
    <li><b>/providers/addjob</b> – Add new job</li>
    <li><b>/users/job/&lt;id&gt;</b> – Job details & application</li>
    <li><b>/logout</b> – Logout and clear session</li>
</ul>





</body>
</html>
