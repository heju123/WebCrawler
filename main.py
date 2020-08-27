from App import create_app


app = create_app()

if __name__ == '__main__':
    # 启动项目
    app.run(debug=True,
            port='8889',
            host='127.0.0.1',
            )
