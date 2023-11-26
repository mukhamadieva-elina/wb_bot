def session_decorator(func):
    def wrapped(self, *args, **kwargs):
        session = self.session()
        kwargs["session"] = session
        try:
            res = func(self, *args, **kwargs)
            session.commit()
            return res
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    return wrapped

def session_decorator_nested(func):
    def wrapped(self, *args, **kwargs):
        if kwargs.get("session") is None:
            session = self.session()
            kwargs["session"] = session
            try:
                res = func(self, *args, **kwargs)
                session.commit()
                return res
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
        else:
            res = func(self, *args, **kwargs)
            return res

    return wrapped
