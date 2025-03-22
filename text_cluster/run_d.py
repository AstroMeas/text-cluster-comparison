def main(host):
    """start dash app"""
    import dash_app
    print('#################################################')

    print('\n' + 'App runs on localhost http://127.0.0.1:8050/' + '\n')

    print('#################################################')
    dash_app.run_app(host)


if __name__ == "__main__":
    main('0.0.0.0')
