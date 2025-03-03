# from sqlalchemy import Column, Integer, String, DECIMAL, Text
# from sqlalchemy.orm import relationship
# from base import Base  # Ensure you're using the same Base

# class Outvoucher(Base):
#     __tablename__ = "outvouchers"  # Adjusted table name to reflect "Outvoucher"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     voucher_id = Column(Integer, nullable=True)  # Assuming this is a legacy or alternate ID
#     voucher_no = Column(String(50), nullable=False, unique=True)  # e.g., #LL9378
#     issue_slip_no = Column(String(50), nullable=True)  # e.g., SLIP98765
#     sale_order_no = Column(String(50), nullable=True)  # e.g., SO123456
#     transport = Column(String(100), nullable=True)  # e.g., DHL
#     vehicle_no = Column(String(50), nullable=True)  # e.g., PB 08: 1014
#     number_of_packages = Column(Integer, nullable=True)  # e.g., 2
#     ordered_by = Column(String(100), nullable=True)  # e.g., Johny
#     sales_person = Column(String(100), nullable=True)  # e.g., John
#     freight_amount = Column(DECIMAL(10, 2), nullable=True, default=0.00)  # e.g., 200
#     remarks = Column(Text, nullable=True)  # Optional remarks/notes
#     receiver_name = Column(String(100), nullable=True)  # Receiver Name
#     mobile_number = Column(String(20), nullable=True)  # Mobile Number

#     # Relationship to OutvoucherItem (assuming items link to this table via voucher_id)
#     items = relationship("OutvoucherItem", back_populates="outvoucher")