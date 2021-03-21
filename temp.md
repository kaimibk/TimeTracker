from home.models import TaskAuthorization, ChargeCode

cc = ChargeCode(name="Test 1", code="TEST", color="#00ffff")
cc.save()
ta = TaskAuthorization(id=1, hours_allocated=10, hours_spent=0, start_date="2020-10-01", end_date="2020-10-31", hours_remaining=10, hours_percentage=0, charge_code=cc)
ta.save()


cc = ChargeCode(name="Test 2", code="TEST TEST", color="#ff0000")
cc.save()
ta = TaskAuthorization(id=2, hours_allocated=10, hours_spent=0, start_date="2020-10-01", end_date="2020-10-31", hours_remaining=10, hours_percentage=0, charge_code=cc)
ta.save()


cc = ChargeCode(name="Test 3", code="TEST TEST TEST", color="#00ff00")
cc.save()
ta = TaskAuthorization(id=3, hours_allocated=10, hours_spent=0, start_date="2020-10-01", end_date="2020-10-31", hours_remaining=10, hours_percentage=0, charge_code=cc)
ta.save()
