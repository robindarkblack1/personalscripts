<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#1d1d1d">
    <title>Dynamic Dashboard</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
    <link rel="stylesheet" href={{url_for('static', filename='css/webfont.css' )}}>
    <link rel="stylesheet" href={{url_for('static', filename='css/main.css' )}}>
    <link rel="stylesheet" href={{url_for('static', filename='css/todo_result.css' )}}>

</head>

<body>
    <nav class="nav">
        <ul class="top-menu">
            <li><a href="#" class="top-link">My-Website</a></li>
            <li class="user-menu">
                <a href="#" class="top-link">Howdy, {{info.firstname}} {{info.lastname}}
                    <i class="bi bi-caret-down-fill u-icon"></i>
                </a>
                <ul class="dropdown-user">
                    <li><a href="#"><i class="bi bi-at top-icon"></i>{{info.username}}</a></li>
                    <li><a href="#"><i class="bi bi-person top-icon"></i>{{info.firstname}}
                            {{info.lastname}}</a></li>
                    <li><a href="/logout"><i class="bi bi-box-arrow-left top-icon"></i> Logout</a></li>
                </ul>
            </li>
        </ul>
    </nav>


    <div class="dashboard">
        <nav class="sidebar">
            <ul class="menu">
                <li><a href="/dashboard"><i class="bi bi-speedometer2 dash-fill"></i><span> Dashboard</span></a></li>
                <li><a href="/media"><i class="bi bi-camera media"></i><span>Media</span></a></li>
                <li class="dropdown">
                    <a href="#" id="dropdown-toggle"><i class="bi bi-grid tools"></i><span> Tools
                            <i class="bi bi-caret-down d-icon"></i>
                            <i class="bi bi-caret-up d-icon" style="display: none;"></i>
                        </span>
                    </a>
                    <ul class="dropdown-menu">
                        <li><a href="/page"><i class="bi bi-list-check"></i><span>
                                    Todo</span></a></li>
                        <li><a href="/error"><i class="bi bi-file-earmark"></i><span>MyTodos</span></a></li>
                        <li><a href="/error"><i class="bi bi-robot"></i><span>
                                    ChatBot</span></a></li>
                    </ul>
                </li>
                <li><a href="/error"><i class="bi bi-graph-up-arrow analytics"></i><span>
                            Analytics</span></a></li>
                <li><a href="/error"><i class="bi bi-people users"></i><span>
                            Users</span></a></li>
                <li class="dropdown">
                    <a href="/error" id="d-toggle">
                        <i class="bi bi-person-vcard profile"></i><span> Profile
                            <i class="bi bi-caret-down d-icon"></i>
                            <i class="bi bi-caret-up d-icon" style="display: none;"></i>
                        </span>
                    </a>
                    <ul class="dropdown-menu">
                        <li><a href="/error"><i class="bi bi-palette themes"></i><span>
                                    Themes</span></a></li>
                    </ul>
                </li>
                <li><a href="/error"><i class="bi bi-gear settings"></i><span>
                            Settings</span></a></li>
                <li><a href="/logout"><i class="bi bi-box-arrow-left logout"></i><span>
                            Logout</span></a></li>
                <button id="toggleSidebar"><i class="bi bi-arrow-left"></i>
                    <li>Collapse Menu</li>
                </button>
            </ul>
        </nav>
            <section class="result">
                {% if name|length == 0 %}
                <div class="alert">
                    No Record Found
                </div>
                {% else %}
                <h3>My Todo</h3>
                <table class="table">
                    <thead>
                        <tr>
                            <th scope="col">S.No</th>
                            <th scope="col">Title</th>
                            <th scope="col">Description</th>
                            <th scope="col">Date Create</th>
                            <th scope="col text-center">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for todo in name %}
                        <tr>
                            <td>{{ loop.index }}</td>
                            <td>{{ todo.title }}</td>
                            <td>{{ todo.desc }}</td>
                            <td>{{ todo.get_ist_time() }}</td>
                            <td>
                                <a href="/update/{{ todo.id }}"><button type="button"
                                        class="update-btn">Update</button></a>
                                <a href="/delete/{{ todo.id }}"><button type="button"
                                        class="delete-btn">Delete</button></a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% endif %}
            </section>
    </div>

</body>

<script src="{{url_for('static', filename='js/script.js' )}}"></script>

</html>