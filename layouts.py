import dash_bootstrap_components as dbc
import dash_html_components as html

from pages.home import home_page

DIRECTORY = {
    "Home": home_page,
}


def make_nav_item(comp_id, name, href):
    return dbc.NavItem(
        children=dbc.NavLink(
            id=comp_id,
            children=name,
            href=href
            )
        )


navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="", height="30px")),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "TokenSets Tracker", className="ml-2 strong"
                            )
                        ),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                # href="\\",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [make_nav_item(x, x, "\\" + x) for x in DIRECTORY],
                    className="ml-auto",
                    navbar=True,
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-5",
)


def page_not_found(pathname):
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )