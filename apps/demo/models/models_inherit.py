from utils.orm.db import BaseModel


class DemoModel(BaseModel):
    __tablename__ = 'demo_model'
    __table_args__ = {'extend_existing': True}
    _inherit = "demo.model"

    async def demo_method(self):
        await super(DemoModel, self).demo_method()
        print('demo inherit')