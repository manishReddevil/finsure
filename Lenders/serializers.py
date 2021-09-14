from rest_framework import serializers
from Lenders.models import Lenders
import csv

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate(self, attrs):
        super().validate(attrs)
        file = attrs['file']
        extension = file.name.split(".")[-1] # splitting the file name that is being uploaded and taking the last string
        if extension != 'csv': # checking the extension of the file and raising a validation error
            raise serializers.ValidationError({'file': 'Please upload a CSV file.'})
        # creating a list to show the correct format of headers
        valid_column = ['Name', 'Code', 'Upfront Commission Rate', 'Trial Commission Rate', 'Active Status']
        decoded_file = file.read().decode('utf-8').splitlines()
        self.csv_reader = csv.DictReader(decoded_file) # reading the file using the csv import
        headers = self.csv_reader.fieldnames
        if headers != valid_column: # checking if the headers match the pre defined header (valid_column)
            raise serializers.ValidationError({'file': 'This file is not valid.'})
        return attrs

    def create(self, validated_data):
        # Created the column_mapper to show the format that is taken to write the data.
        # Code written in line 37 canbe used too.
        column_mapper = {
            'Name': 'name',
            'Code': 'code',
            'Upfront Commission Rate': 'upfront_commission_rate',
            'Trial Commission Rate': 'trial_commission_rate',
            'Active Status': 'active'
        }
        lenders = []
        for row in self.csv_reader:
            lender = dict()
            # lenders.append(Lenders(name=row['Name'], code=row['Code']))
            for k, v in row.items():
                lender[column_mapper.get(k)] = v.strip() if k != 'Active Status' else eval(v.title())
            lenders.append(Lenders(**lender))

        Lenders.objects.bulk_create(lenders, batch_size=200)
        return validated_data


class FileDownloadSerializer(serializers.Serializer):
    pass


class LendersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lenders
        fields = '__all__'
