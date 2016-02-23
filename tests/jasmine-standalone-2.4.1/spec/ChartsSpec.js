describe("getFetchedData 1", function() {
  it("non-null data passed from Python", function() {
      expect(getFetchedData).not.toBe(null);
  });
});

// describe("getFetchedData 2", function() {
//   it("value of data passed from Python without quotation marks, check if expected", function() {
//       var data = getFetchedData;
//       data.replace('/\'/g', '').replace(/\"\"/g, '');
//       var data_no_strings = "{result: [{time: 3, _id: {$oid: 56cbaf551bad1a44a406a633}, type: quiz_result, score: 99, name: testQuizName3}, {time: 2, _id: {$oid: 56cbaf551bad1a44a406a632}, type: quiz_result, score: 80, name: testQuizName2}, {time: 1, _id: {$oid: 56cbaf551bad1a44a406a631}, type: quiz_result, score: 90, name: testQuizName1}]}";
//       expect(data).toEqual(data_no_strings);
//   });
// });

// describe("getFetchedData 3", function() {
//   it("value of data passed from Python contains some expected values", function() {
//       var data = getFetchedData;
//       var aValue = "testQuizName1";
//       expect(data).toContain(aValue);
//   });
// });

// describe("getFetchedData 4", function() {
//   it("defined data passed from Python", function() {
//       expect(data).toBeDefined();
//   });
// });
