\# Data Model - Star Schema



\## Overview

This module builds the Data Warehouse dimensional model (Star Schema).



\## ERD Diagram

!\[Star Schema ERD](erd\_star\_schema\_detailed.html)



\## Tables



\### Fact Table

\*\*fact\_sales\*\* — contains all sales transactions

| Column | Type | Description |

|--------|------|-------------|

| order\_id | FK | رقم الطلب |

| customer\_id | FK | رقم العميل |

| product\_id | FK | رقم المنتج |

| store\_id | FK | رقم الفرع |

| date\_id | FK | رقم التاريخ |

| quantity | int | الكمية |

| list\_price | float | السعر |

| discount | float | الخصم |

| total\_price | float | الإجمالي |



\### Dimension Tables

| Table | Description |

|-------|-------------|

| dim\_customer | بيانات العملاء |

| dim\_product | المنتجات + brands + categories |

| dim\_store | الفروع + عدد الموظفين |

| dim\_date | التواريخ بكل تفاصيلها |



\## Why Star Schema?

\- الاستعلامات أسرع

\- التصميم أبسط

\- سهل الـ Reporting

