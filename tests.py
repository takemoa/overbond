import unittest
from datetime import datetime
from io import StringIO

from log_utils import setup_logging_for_test
from parse_utils import parse_record

# A test record to be used in below test
test_record = \
    'BDSr;i2;NAmGITS;\n' \
    'BDx;i138;Si6;s2;SYmIS;NAmNasdaq Iceland hf.;CNyIS;MIcXICE;\n' \
    'BDm;i896;Si006178;s2;Ex138;NAmIceland Cash Bond Trading;SYmICECB;TOTa+0000;LDa20190406;MIcXICE;\n' \
    'BDIs;i14996;SiMOS;s2;ISsMOS;NAmMosfellsbær;CNyIS;MLEi2549007HX5IIWNKYNB91;\n' \
    'BDt;i8211;SiMOS_99_1;s2;Ex138;Mk896;INiMOS005ICECBCSH;SYmMOS 99 1;NAmMosfellsbær 99 1;SNmMOS 99 1;ISnIS0000003960;ISi14996;ISsMOS;CUiISK;CUtISK;PRt3;VOd2;LDa20001028;Cf1;TTd20240620;CFcDNFUFB;IEtOther;NMv1;ITSz347;NDp4;NDc3;MPmN;MPaN;NDTp4;NDTc3;CLId21232;CNyIS;ITStN;SSc2;STy4;AUmY;TRaY;INrY;PTaN;PTb2;OXCl0;RLoY;IaN;FxN;IqN;TUsN;MSc444;LSz5000000;\n' \
    'BDu;i8211;SiMOS_99_1;s2;IICtISIN;FISnMOSFELLSBAER/4.75 BD 20240620;MIFrBOND;MCTyOTHR;MLIqN;MTcN;MLPr100000000;MLPo0;MSPo0;MJCjN;MQu10000;MBTyOEPB;MBPs0;MCStN;\n' \
    'BDBo;i8211;SiMOS_99_1;s2;BTy1;DIs19990507;AOs200000000;DMa20240620;RCp4.75;DNc20220620;DCm1;Mv100;HaY;RDd0;RDt1;NRd2;CPFrN;LCOd20240620;Fv1;CFq1;Cc8;RIxCPI_IS;FCd20000620;VBa186.4;Vm5000000;MDo255;SSDaN;FIt3;DAd19990507;\n' \
    'BDLi;i14718;SiISMB;s2;LSt433;SYmISMB;NAmICE Municipal and LSS Bonds;LCyISK;TCeY;\n' \
    'BDLi;i14720;SiICE_MUNICIPAL_AND_LSS_BONDS;s2;LSt434;PAi14718;NAmICE Municipal and LSS Bonds;LCyISK;TCeN;\n' \
    'm;i8211;t180000.336;Dt20210907;ISOcY;ISOtY;\n'

# Setup logging here
setup_logging_for_test()


# test case class
class TestCase(unittest.TestCase):

    # Test parse_utils.parse_record
    def test_parse_record(self):
        with StringIO(test_record) as fp:
            sr = parse_record(fp)
            # {'TradingType': 'Iceland Cash Bond Trading', 'RIKS': 'MOS 99 1', 'ISIN': 'IS0000003960',
            #  'Issue_Currency': 'ISK', 'Trading_Currency': 'ISK',
            #  'Last_trading_Day': datetime.datetime(2024, 6, 20, 0, 0),
            #  'Issuance_Date': datetime.datetime(1999, 5, 7, 0, 0), 'Amount_Outstanding': 200000000.0,
            #  'Coupon_Rate': 4.75, 'Maturity_Date': datetime.datetime(2022, 6, 20, 0, 0),
            #  'Next_Coupon_Date': datetime.datetime(2022, 6, 20, 0, 0), 'Redeem_Value': 100.0,
            #  'Last_Coupon_Date': datetime.datetime(2024, 6, 20, 0, 0), 'Number_of_Coupons': 1.0, 'Base_Value': 186.4,
            #  'Name': 'ICE Municipal and LSS Bonds', 'DataDATE': datetime.datetime(2021, 9, 7, 0, 0)}
            self.assertEqual(sr.get('ISIN'), 'IS0000003960')
            self.assertEqual(sr.get('Name'), 'ICE Municipal and LSS Bonds')
            self.assertEqual(sr.get('DataDATE'), datetime(2021, 9, 7, 0, 0))
            self.assertEqual(sr.get('Amount_Outstanding'), 200000000)
            # TODO add all fields


if __name__ == '__main__':
    unittest.main()
