def main(host):
    """start dash app"""
    import dash_app
    dash_app.run_app(host)


if __name__ == "__main__":
    main('0.0.0.0')
