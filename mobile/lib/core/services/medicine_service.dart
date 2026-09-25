import 'package:dio/dio.dart';
import '../constants/api_constants.dart';
import 'api_service.dart';

class MedicineModel {
  final String id;
  final String brandName;
  final String genericName;
  final String? manufacturer;
  final String? strength;
  final String? dosageForm;
  final String? barcode;
  final double? mrp;
  final bool requiresPrescription;

  MedicineModel({
    required this.id,
    required this.brandName,
    required this.genericName,
    this.manufacturer,
    this.strength,
    this.dosageForm,
    this.barcode,
    this.mrp,
    required this.requiresPrescription,
  });

  factory MedicineModel.fromJson(Map<String, dynamic> json) {
    final mrpValue = json['mrp'];
    return MedicineModel(
      id: json['id']?.toString() ?? '',
      brandName: json['brand_name']?.toString() ?? '',
      genericName: json['generic_name']?.toString() ?? '',
      manufacturer: json['manufacturer']?.toString(),
      strength: json['strength']?.toString(),
      dosageForm: json['dosage_form']?.toString(),
      barcode: json['barcode']?.toString(),
      mrp: mrpValue is num ? mrpValue.toDouble() : null,
      requiresPrescription: json['requires_prescription'] as bool? ?? false,
    );
  }
}

class MedicineService {
  final _api = ApiService();

  Future<List<MedicineModel>> searchMedicines(String query) async {
    try {
      final response = await _api.dio.get(
        ApiConstants.medicineSearch,
        queryParameters: {'q': query, 'limit': 20},
      );
      final data = response.data as Map<String, dynamic>;
      final medicines = data['medicines'] as List<dynamic>? ?? [];
      return medicines
          .map(
            (medicine) =>
                MedicineModel.fromJson(medicine as Map<String, dynamic>),
          )
          .toList();
    } on DioException catch (e) {
      throw Exception('Search failed: ${e.message}');
    }
  }

  Future<MedicineModel?> getMedicineByBarcode(String barcode) async {
    try {
      final response = await _api.dio.get(
        '${ApiConstants.medicineBarcode}/$barcode',
      );
      return MedicineModel.fromJson(response.data as Map<String, dynamic>);
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) return null;
      throw Exception('Lookup failed: ${e.message}');
    }
  }
}
