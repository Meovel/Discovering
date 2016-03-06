describe("test data is fetched from Parse in queryToChart 1", function() {
  it("non-null data passed from Parse to queryToChart", function() {
    expect(queryToChart()).not.toBe(null);
  })
})

describe("test data is fetched from Parse in queryToChart 2", function() {
  it("non-empty data passed from Parse to queryToChart", function() {
    expect(queryToChart()).not.toBe([]);
  })
})

describe("test data is fetched from Parse in queryToChart 3", function() {
  it("defined data passed from Parse to queryToChart", function() {
    expect(queryToChart()).toBeDefined();
  })
})

describe("test data is fetched from Parse in queryToChart 4", function() {
  it("truthy data passed from Parse to queryToChart", function() {
    expect(queryToChart()).toBeDefined();
  })
})

describe("test data is fetched from Parse in queryToChart 5", function() {
  it("non-null json at first entry of array from data passed from Parse to queryToChart", function() {
    expect(queryToChart()[0]).not.toBe(null);
  })
})
