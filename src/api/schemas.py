"""Contains the Schemas for various messages."""
from pydantic import BaseModel, validator


class ApplicationData(BaseModel):
    """Request schema."""

    sk_id_curr: int
    amt_annuity: float
    amt_credit: float
    amt_goods_price: float
    amt_income_total: float
    amt_req_credit_bureau_day: float
    amt_req_credit_bureau_hour: float
    amt_req_credit_bureau_mon: float
    amt_req_credit_bureau_qrt: float
    amt_req_credit_bureau_week: float
    amt_req_credit_bureau_year: float
    cnt_children: int
    cnt_fam_members: float
    code_gender: str
    days_birth: float
    days_employed: float
    days_id_publish: float
    days_last_phone_change: float
    days_registration: float
    def_30_cnt_social_circle: float
    def_60_cnt_social_circle: float
    ext_source_1: float
    ext_source_2: float
    ext_source_3: float
    flag_cont_mobile: float
    flag_document_10: float
    flag_document_11: float
    flag_document_12: float
    flag_document_13: float
    flag_document_14: float
    flag_document_15: float
    flag_document_16: float
    flag_document_17: float
    flag_document_18: float
    flag_document_19: float
    flag_document_2: float
    flag_document_20: float
    flag_document_21: float
    flag_document_3: float
    flag_document_4: float
    flag_document_5: float
    flag_document_6: float
    flag_document_7: float
    flag_document_8: float
    flag_document_9: float
    flag_email: float
    flag_emp_phone: float
    flag_mobil: float
    flag_own_car: str
    flag_own_realty: str
    flag_phone: float
    flag_work_phone: float
    hour_appr_process_start: float
    live_city_not_work_city: float
    live_region_not_work_region: float
    name_contract_type: str
    name_education_type: str
    name_family_status: str
    name_housing_type: str
    name_income_type: str
    name_type_suite: str
    obs_30_cnt_social_circle: float
    obs_60_cnt_social_circle: float
    occupation_type: str
    organization_type: str
    reg_city_not_live_city: float
    reg_city_not_work_city: float
    reg_region_not_live_region: float
    reg_region_not_work_region: float
    region_population_relative: float
    region_rating_client_w_city: float
    region_rating_client: float
    weekday_appr_process_start: str

    @validator("code_gender")
    def check_gender(cls, gender: str) -> str:
        """Verify city is supported."""
        pass

    class Config:
        """Request config."""

        schema_extra = {
            "example": {
                "sk_id_curr": 100002,
                "amt_annuity": 24700.5,
                "amt_credit": 406597.5,
                "amt_goods_price": 351000.0,
                "amt_income_total": 202500.0,
                "amt_req_credit_bureau_day": 0.0,
                "amt_req_credit_bureau_hour": 0.0,
                "amt_req_credit_bureau_mon": 0.0,
                "amt_req_credit_bureau_qrt": 0.0,
                "amt_req_credit_bureau_week": 0.0,
                "amt_req_credit_bureau_year": 1.0,
                "cnt_children": 0,
                "cnt_fam_members": 1.0,
                "code_gender": "m",
                "days_birth": -9461,
                "days_employed": -637.0,
                "days_id_publish": -2120,
                "days_last_phone_change": -1134.0,
                "days_registration": -3648.0,
                "def_30_cnt_social_circle": 2.0,
                "def_60_cnt_social_circle": 2.0,
                "ext_source_1": 0.0830369673913225,
                "ext_source_2": 0.2629485927471776,
                "ext_source_3": 0.1393757800997895,
                "flag_cont_mobile": 1,
                "flag_document_10": 0,
                "flag_document_11": 0,
                "flag_document_12": 0,
                "flag_document_13": 0,
                "flag_document_14": 0,
                "flag_document_15": 0,
                "flag_document_16": 0,
                "flag_document_17": 0,
                "flag_document_18": 0,
                "flag_document_19": 0,
                "flag_document_2": 0,
                "flag_document_20": 0,
                "flag_document_21": 0,
                "flag_document_3": 1,
                "flag_document_4": 0,
                "flag_document_5": 0,
                "flag_document_6": 0,
                "flag_document_7": 0,
                "flag_document_8": 0,
                "flag_document_9": 0,
                "flag_email": 0,
                "flag_emp_phone": 1,
                "flag_mobil": 1,
                "flag_own_car": "n",
                "flag_own_realty": "y",
                "flag_phone": 1,
                "flag_work_phone": 0,
                "hour_appr_process_start": 10,
                "live_city_not_work_city": 0,
                "live_region_not_work_region": 0,
                "name_contract_type": "cash loans",
                "name_education_type": "secondary / secondary special",
                "name_family_status": "single / not married",
                "name_housing_type": "house / apartment",
                "name_income_type": "working",
                "name_type_suite": "unaccompanied",
                "obs_30_cnt_social_circle": 2.0,
                "obs_60_cnt_social_circle": 2.0,
                "occupation_type": "laborers",
                "organization_type": "business entity type 3",
                "reg_city_not_live_city": 0,
                "reg_city_not_work_city": 0,
                "reg_region_not_live_region": 0,
                "reg_region_not_work_region": 0,
                "region_population_relative": 0.018801,
                "region_rating_client_w_city": 2,
                "region_rating_client": 2,
                "weekday_appr_process_start": "wednesday",
            }
        }


class ResponseData(BaseModel):
    """Response schema."""

    sk_id_curr: int
    prob_default: float
    prediction: int

    class Config:
        """Response config."""

        schema_extra = {
            "example": {"sk_id_curr": 100002, "prob_default": 0.12, "prediction": 1}
        }
