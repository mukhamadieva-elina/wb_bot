def session_decorator(func):

    async def wrapped(self, *args, **kwargs):
        session = self.session()
        kwargs["session"] = session
        try:
            res = await func(self, *args, **kwargs)
            await session.commit()
            return res
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

    return wrapped


def session_decorator_nested(func):
    async def wrapped(self, *args, **kwargs):
        if kwargs.get("session") is None:
            session = self.session()
            kwargs["session"] = session
            try:
                res = await func(self, *args, **kwargs)
                await session.commit()
                return res
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
        else:
            res = await func(self, *args, **kwargs)
            return res

    return wrapped
